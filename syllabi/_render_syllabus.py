"""Render the Summer 2026 syllabus Markdown to a styled, self-contained HTML file."""
import markdown

SRC = "syllabus_su26.md"
OUT = "syllabus_su26.html"

with open(SRC, encoding="utf-8") as f:
    md_text = f.read()

body = markdown.markdown(
    md_text,
    extensions=["extra", "sane_lists", "toc", "nl2br"],
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COMP 1150 — Computer Science Concepts (Summer 2026)</title>
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
    max-width: 860px;
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
  ul, ol {{ padding-left: 1.5rem; }}
  li {{ margin: 0.25rem 0; }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
  strong {{ color: #14222e; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .page {{ box-shadow: none; max-width: none; padding: 0; }}
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

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {OUT} ({len(html):,} bytes)")
