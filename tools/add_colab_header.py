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


def strip_dividers(source) -> list[str]:
    """Remove standalone `---` lines (markdown horizontal rules / cell dividers).

    Notebook `source` may be a single string OR a list of line strings;
    normalize before splitting so we never iterate over characters.
    """
    if isinstance(source, str):
        text = source
    else:
        text = "".join(source)
    lines = text.splitlines(keepends=True)
    return [ln for ln in lines if ln.strip() != "---"]


def normalize_form_cells(cells: list) -> None:
    """Sync metadata for `#@title`-marked code cells across Colab + Quarto.

    A code cell whose `#@title` line appears anywhere in its leading
    comments is treated as a hide-by-default helper cell (diagrams,
    arcade generators, etc.). The function:

      - Sets Colab metadata (`cellView: form` + `jupyter.source_hidden`)
        so the cell collapses to a title bar in Colab.
      - Injects a Quarto cell directive on line 1 — `#| echo: false`
        for cells with saved outputs (keeps the diagram, hides the
        code) or `#| include: false` for output-less cells (drops the
        cell entirely, used for interactive arcades).

    The Quarto directive must be the first line of the cell, so the
    `#@title` line is pushed to line 2. Colab's form mode is triggered
    by `cellView: form` (metadata, not source order), so this still
    collapses correctly in Colab.

    When the `#@title` line is removed, the cleanup undoes both the
    metadata and the injected directive, so the script is reversible
    and idempotent.
    """
    QUARTO_TAGS = ("remove-input", "remove-cell")
    MANAGED_DIRECTIVES = ("#| echo: false", "#| include: false")
    for c in cells:
        if c.get("cell_type") != "code":
            continue
        src = c.get("source", "")
        text = "".join(src) if isinstance(src, list) else src
        lines = text.splitlines(keepends=True)

        # Strip any previously-managed directive so re-runs don't stack.
        while lines and lines[0].strip() in MANAGED_DIRECTIVES:
            lines.pop(0)

        has_title = any(
            ln.lstrip().startswith("#@title") for ln in lines[:5]
        )

        md = c.setdefault("metadata", {})
        tags = [t for t in md.get("tags", []) if t not in QUARTO_TAGS]

        if has_title:
            md["cellView"] = "form"
            md.setdefault("jupyter", {})["source_hidden"] = True
            directive = "#| echo: false\n" if c.get("outputs") else "#| include: false\n"
            lines.insert(0, directive)
        else:
            md.pop("cellView", None)
            jup = md.get("jupyter") or {}
            jup.pop("source_hidden", None)
            if not jup:
                md.pop("jupyter", None)
            else:
                md["jupyter"] = jup

        if tags:
            md["tags"] = tags
        else:
            md.pop("tags", None)
        c["source"] = lines


def update_notebook(path: Path, repo_root: Path) -> bool:
    rel_path = path.relative_to(repo_root).as_posix()
    original = path.read_text(encoding="utf-8")
    nb = json.loads(original)
    cells = nb.get("cells", [])
    new_cell = make_cell(rel_path)

    for c in cells:
        if c.get("cell_type") == "markdown" and MARKER not in "".join(c.get("source", [])):
            c["source"] = strip_dividers(c.get("source", []))

    normalize_form_cells(cells)

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
