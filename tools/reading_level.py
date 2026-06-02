#!/usr/bin/env python3
"""Estimate reading grade levels for course materials.

Extracts *prose* (markdown text) from Jupyter notebooks (.ipynb) and Quarto
documents (.qmd), strips out code, then reports readability scores:

  - Flesch-Kincaid Grade Level   (US grade)
  - Flesch Reading Ease          (0-100, higher = easier)
  - Gunning Fog Index            (US grade)
  - SMOG Index                   (US grade)

No third-party dependencies required.

Usage:
    python tools/reading_level.py                      # scan v2/ by default
    python tools/reading_level.py path/to/file.ipynb   # one or more files
    python tools/reading_level.py v2/notebooks v2/cases # dirs (recursive)
    python tools/reading_level.py --csv scores.csv ...  # also write a CSV
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Text extraction
# --------------------------------------------------------------------------- #

def extract_from_ipynb(path: Path) -> str:
    """Return concatenated markdown-cell text from a notebook."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    chunks = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            chunks.append("".join(cell.get("source", [])))
    return "\n\n".join(chunks)


def extract_from_qmd(path: Path) -> str:
    """Return prose from a Quarto/Markdown file, minus code and metadata."""
    text = path.read_text(encoding="utf-8")
    # Drop YAML front matter (--- ... --- at the very top).
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    return text


def clean_markdown(text: str) -> str:
    """Strip markdown/code syntax so only readable prose remains."""
    # Fenced code blocks (``` or ~~~), including Quarto ```{python} cells.
    text = re.sub(r"(?ms)^[ \t]*([`~]{3,}).*?^[ \t]*\1[ \t]*$", " ", text)
    # Inline code.
    text = re.sub(r"`[^`]*`", " ", text)
    # Images / links: keep the visible text, drop the target.
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)
    # LaTeX math.
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$\n]*\$", " ", text)
    # Heading markers, blockquotes, list bullets, table pipes.
    text = re.sub(r"(?m)^[ \t]*#{1,6}[ \t]*", "", text)
    text = re.sub(r"(?m)^[ \t]*>+[ \t]*", "", text)
    text = re.sub(r"(?m)^[ \t]*([-*+]|\d+\.)[ \t]+", "", text)
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"(?m)^[ \t]*[-:| ]{3,}[ \t]*$", " ", text)  # table separators
    # Emphasis / strikethrough markers.
    text = re.sub(r"[*_~]{1,3}", "", text)
    return text


# --------------------------------------------------------------------------- #
# Tokenizing + syllable counting
# --------------------------------------------------------------------------- #

_SENTENCE_RE = re.compile(r"[^.!?]*[.!?]+|[^.!?]+$")
_WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def count_syllables(word: str) -> int:
    """Heuristic English syllable count (good enough for readability stats)."""
    word = word.lower()
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    # Silent trailing 'e' (but not 'le' as in "table").
    if word.endswith("e") and not word.endswith("le") and count > 1:
        count -= 1
    return max(count, 1)


def analyze(text: str) -> dict | None:
    sentences = [s.strip() for s in _SENTENCE_RE.findall(text) if s.strip()]
    words = _WORD_RE.findall(text)
    if not words or not sentences:
        return None

    syllables = [count_syllables(w) for w in words]
    n_words = len(words)
    n_sentences = len(sentences)
    n_syllables = sum(syllables)
    complex_words = sum(1 for s in syllables if s >= 3)

    words_per_sentence = n_words / n_sentences
    syllables_per_word = n_syllables / n_words

    fk_grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    reading_ease = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    fog = 0.4 * (words_per_sentence + 100 * complex_words / n_words)
    smog = 1.043 * ((complex_words * (30 / n_sentences)) ** 0.5) + 3.1291

    return {
        "words": n_words,
        "sentences": n_sentences,
        "fk_grade": round(fk_grade, 1),
        "reading_ease": round(reading_ease, 1),
        "fog": round(fog, 1),
        "smog": round(smog, 1),
    }


# --------------------------------------------------------------------------- #
# Driving the files
# --------------------------------------------------------------------------- #

def score_file(path: Path) -> dict | None:
    if path.suffix == ".ipynb":
        raw = extract_from_ipynb(path)
    elif path.suffix in (".qmd", ".md", ".markdown"):
        raw = extract_from_qmd(path)
    else:
        return None
    result = analyze(clean_markdown(raw))
    if result:
        result["file"] = str(path)
    return result


def gather_files(targets: list[str]) -> list[Path]:
    exts = {".ipynb", ".qmd", ".md", ".markdown"}
    files: list[Path] = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            files.extend(f for f in sorted(p.rglob("*")) if f.suffix in exts)
        elif p.is_file():
            files.append(p)
        else:
            print(f"warning: no such path: {t}", file=sys.stderr)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", default=["v2"],
                        help="files or directories to scan (default: v2)")
    parser.add_argument("--csv", metavar="FILE", help="write results to a CSV file")
    parser.add_argument("--sort", choices=["file", "grade"], default="file",
                        help="sort output by filename or FK grade (default: file)")
    args = parser.parse_args()

    files = gather_files(args.paths or ["v2"])
    rows = [r for f in files if (r := score_file(f))]
    if not rows:
        print("No readable content found.", file=sys.stderr)
        return 1

    if args.sort == "grade":
        rows.sort(key=lambda r: r["fk_grade"], reverse=True)

    name_w = max(len(Path(r["file"]).name) for r in rows)
    header = f"{'File':<{name_w}}  {'Words':>6}  {'FK-Grade':>8}  {'Ease':>5}  {'Fog':>5}  {'SMOG':>5}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{Path(r['file']).name:<{name_w}}  {r['words']:>6}  "
              f"{r['fk_grade']:>8}  {r['reading_ease']:>5}  {r['fog']:>5}  {r['smog']:>5}")

    grades = [r["fk_grade"] for r in rows]
    print("-" * len(header))
    print(f"{'AVERAGE':<{name_w}}  {sum(r['words'] for r in rows):>6}  "
          f"{sum(grades) / len(grades):>8.1f}")

    if args.csv:
        import csv
        cols = ["file", "words", "sentences", "fk_grade", "reading_ease", "fog", "smog"]
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=cols)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nWrote {args.csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
