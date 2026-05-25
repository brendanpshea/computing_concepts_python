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
NOTEBOOK_DIRS = ["summer_2026/notebooks"]
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


def update_notebook(path: Path, repo_root: Path) -> bool:
    rel_path = path.relative_to(repo_root).as_posix()
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    new_cell = make_cell(rel_path)

    existing_idx = next(
        (i for i, c in enumerate(cells)
         if c.get("cell_type") == "markdown"
         and MARKER in "".join(c.get("source", []))),
        None,
    )

    if existing_idx is None:
        cells.insert(0, new_cell)
    else:
        if cells[existing_idx].get("source") == new_cell["source"]:
            return False
        cells[existing_idx] = new_cell

    nb["cells"] = cells
    path.write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
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
