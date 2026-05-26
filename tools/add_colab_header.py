"""Insert/refresh a Colab + download header cell at the top of each course notebook.

Idempotent: detects an existing header by the MARKER string and replaces it
instead of stacking duplicates.

Usage:
    python tools/add_colab_header.py
    python tools/add_colab_header.py --check   # exit 1 if any file would change
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = "brendanpshea/computing_concepts_python"
BRANCH = "main"
NOTEBOOK_DIRS = ["v2/notebooks"]
MARKER = "<!-- COLAB-BADGE -->"


def header_source(rel_path: str) -> list[str]:
    colab_url = f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/{rel_path}"
    raw_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{rel_path}"
    gh_url = f"https://github.com/{REPO}/blob/{BRANCH}/{rel_path}"
    badge = "https://colab.research.google.com/assets/colab-badge.svg"
    lines = [
        f"{MARKER}\n",
        f"[![Open In Colab]({badge})]({colab_url})  \n",
        f"[Download .ipynb]({raw_url}) · [View on GitHub]({gh_url})\n",
    ]
    return lines


def make_cell(rel_path: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {"colab_header": True},
        "source": header_source(rel_path),
    }


def strip_dividers(source: list[str]) -> list[str]:
    """Remove standalone `---` lines (markdown horizontal rules / cell dividers).

    These break Quarto's YAML parser when notebooks are rendered, and the
    author doesn't want them. Lines containing only `---` (with optional
    surrounding whitespace) are dropped. Preserves trailing newlines on
    neighboring lines.
    """
    return [ln for ln in source if ln.strip() != "---"]


def update_notebook(path: Path, repo_root: Path) -> bool:
    rel_path = path.relative_to(repo_root).as_posix()
    original = path.read_text(encoding="utf-8")
    nb = json.loads(original)
    cells = nb.get("cells", [])
    new_cell = make_cell(rel_path)

    for c in cells:
        if c.get("cell_type") == "markdown" and MARKER not in "".join(c.get("source", [])):
            c["source"] = strip_dividers(c.get("source", []))

    existing_idx = next(
        (i for i, c in enumerate(cells)
         if c.get("cell_type") == "markdown"
         and MARKER in "".join(c.get("source", []))),
        None,
    )

    if existing_idx is None:
        cells.insert(0, new_cell)
    else:
        cells[existing_idx] = new_cell

    nb["cells"] = cells
    new_text = json.dumps(nb, indent=1, ensure_ascii=False) + "\n"
    if new_text == original:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any notebook would be modified")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    changed: list[str] = []
    for d in NOTEBOOK_DIRS:
        for nb_path in sorted((repo_root / d).glob("*.ipynb")):
            if args.check:
                original = nb_path.read_bytes()
                if update_notebook(nb_path, repo_root):
                    nb_path.write_bytes(original)
                    changed.append(nb_path.as_posix())
            else:
                if update_notebook(nb_path, repo_root):
                    changed.append(nb_path.as_posix())
                    print(f"updated {nb_path.relative_to(repo_root).as_posix()}")

    if args.check and changed:
        print("would update:")
        for c in changed:
            print(f"  {c}")
        return 1
    if not args.check and not changed:
        print("no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
