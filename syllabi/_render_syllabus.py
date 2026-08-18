"""Render a COMP 1150 syllabus Markdown file to a styled, self-contained HTML file.

Usage:
    python _render_syllabus.py                    # renders every syllabus_*.md
    python _render_syllabus.py syllabus_fa26.md   # renders just one
"""
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).parent

TERMS = {
    "su": "Summer",
    "fa": "Fall",
    "sp": "Spring",
}


def page_title(md_text: str, src: Path) -> str:
    """Build the <title> from the '**COMP 1150 | Fall 2026**' line, else the filename."""
    m = re.search(r"\*\*(COMP\s*1150)\s*\|\s*([^*]+)\*\*", md_text)
    if m:
        return f"{m.group(1)} — Computer Science Concepts ({m.group(2).strip()})"
    m = re.match(r"syllabus_([a-z]{2})(\d{2})", src.stem)
    if m:
        return f"COMP 1150 — Computer Science Concepts ({TERMS.get(m.group(1), '')} 20{m.group(2)})"
    return src.stem


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --accent: #1f5f8b;
    --accent-light: #e8f1f8;
    --text: #1c2733;
    --muted: #5a6b7b;
    --border: #d8e0e8;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.65;
    color: var(--text);
    background: #f4f6f9;
    margin: 0;
    padding: 2rem 1rem;
  }}
  .page {{
    max-width: 900px;
    margin: 0 auto;
    background: #fff;
    padding: 3rem 3.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 18px rgba(31, 95, 139, 0.10);
  }}
  h1 {{
    color: var(--accent);
    font-size: 2.1rem;
    margin: 0 0 0.25rem;
    border-bottom: 3px solid var(--accent);
    padding-bottom: 0.5rem;
  }}
  h2 {{
    color: var(--accent);
    margin-top: 2.4rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.3rem;
  }}
  h3 {{ color: #2c4a63; margin-top: 1.8rem; }}
  h4 {{ color: #2c4a63; margin-top: 1.5rem; font-size: 1.05rem; }}
  a {{ color: var(--accent); }}
  code, pre {{
    background: var(--accent-light);
    border-radius: 5px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.92em;
  }}
  code {{ padding: 0.1em 0.35em; }}
  pre {{ padding: 1rem; overflow-x: auto; border-left: 4px solid var(--accent); }}
  pre code {{ background: none; padding: 0; }}
  blockquote {{
    border-left: 4px solid var(--accent);
    margin: 1rem 0;
    padding: 0.4rem 1.2rem;
    background: var(--accent-light);
    color: var(--muted);
  }}
  .table-wrap {{ overflow-x: auto; margin: 1.2rem 0; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 0.95rem;
  }}
  th, td {{
    border: 1px solid var(--border);
    padding: 0.5rem 0.75rem;
    text-align: left;
    vertical-align: top;
  }}
  th {{ background: var(--accent-light); color: #14222e; }}
  tbody tr:nth-child(even) {{ background: #fafcfe; }}
  s {{ color: var(--muted); }}
  ul, ol {{ padding-left: 1.5rem; }}
  li {{ margin: 0.25rem 0; }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
  strong {{ color: #14222e; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .page {{ box-shadow: none; max-width: none; padding: 0; }}
    table {{ page-break-inside: auto; }}
    tr {{ page-break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="page">
{body}
</div>
</body>
</html>
"""


def render(src: Path) -> Path:
    md_text = src.read_text(encoding="utf-8")
    body = markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists", "toc", "nl2br"],
    )
    # Let wide calendar tables scroll rather than blow out the page on phones.
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace(
        "</table>", "</table></div>"
    )
    out = src.with_suffix(".html")
    out.write_text(
        TEMPLATE.format(title=page_title(md_text, src), body=body), encoding="utf-8"
    )
    print(f"Wrote {out.name} ({out.stat().st_size:,} bytes)")
    return out


if __name__ == "__main__":
    targets = [Path(a) for a in sys.argv[1:]] or sorted(HERE.glob("syllabus_*.md"))
    if not targets:
        sys.exit("No syllabus_*.md files found.")
    for t in targets:
        render(t if t.is_absolute() else HERE / t)
