"""Post-render accessibility fixes for the generated site.

Pandoc emits table headers without a `scope` attribute and inlines Graphviz
SVGs with no accessible name, neither of which can be fixed from the .qmd /
.ipynb source. This script patches the rendered HTML instead.

It is wired into _quarto.yml as a post-render step, so `quarto render` keeps
the output accessible. It is idempotent — running it twice changes nothing.

Usage:
    python tools/fix_a11y.py            # patch docs/ (default)
    python tools/fix_a11y.py some.html  # patch specific files
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"

# Skip the theme's own bundled assets; we only own the page markup.
SKIP_PARTS = {"site_libs"}


def add_th_scope(html: str) -> tuple[str, int]:
    """Add scope="col" to header-row cells and scope="row" to stub cells."""
    n = 0

    def scope_within(block: str, value: str) -> str:
        nonlocal n

        def one(m: re.Match) -> str:
            nonlocal n
            attrs = m.group(1)
            if "scope=" in attrs:
                return m.group(0)
            n += 1
            return f'<th scope="{value}"{attrs}>'

        return re.sub(r"<th\b([^>]*)>", one, block)

    # <th> inside <thead> labels a column; anywhere else (a stub cell in
    # <tbody>) labels a row.
    html = re.sub(
        r"<thead\b.*?</thead>",
        lambda m: scope_within(m.group(0), "col"),
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<tbody\b.*?</tbody>",
        lambda m: scope_within(m.group(0), "row"),
        html,
        flags=re.DOTALL,
    )
    return html, n


def label_inline_svg(html: str) -> tuple[str, int]:
    """Name each inline <svg> from its own <figcaption>, per WCAG 1.1.1."""
    n = 0

    def one_figure(m: re.Match) -> str:
        nonlocal n
        fig = m.group(0)
        if "<svg" not in fig:
            return fig
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", fig, re.DOTALL)
        if not cap:
            return fig
        text = re.sub(r"<[^>]+>", "", cap.group(1))
        text = " ".join(text.split()).replace('"', "&quot;")
        if not text:
            return fig

        def one_svg(sm: re.Match) -> str:
            nonlocal n
            attrs = sm.group(1)
            if re.search(r"aria-label|aria-labelledby|role=", attrs):
                return sm.group(0)
            n += 1
            return f'<svg role="img" aria-label="{text}"{attrs}>'

        return re.sub(r"<svg\b([^>]*)>", one_svg, fig, count=1)

    html = re.sub(r"<figure\b.*?</figure>", one_figure, html, flags=re.DOTALL)
    return html, n


def patch(path: Path) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    html, n_scope = add_th_scope(original)
    html, n_svg = label_inline_svg(html)
    if html != original:
        path.write_text(html, encoding="utf-8")
    return n_scope, n_svg


def main(argv: list[str]) -> int:
    if argv:
        targets = [Path(a) for a in argv]
    else:
        targets = [
            p
            for p in SITE.rglob("*.html")
            if not SKIP_PARTS.intersection(p.relative_to(SITE).parts)
        ]
    if not targets:
        print("fix_a11y: nothing to patch")
        return 0

    files, scopes, svgs = 0, 0, 0
    for p in targets:
        a, b = patch(p)
        if a or b:
            files += 1
            scopes += a
            svgs += b
    print(
        f"fix_a11y: {scopes} th scoped, {svgs} svg labeled, "
        f"across {files} of {len(targets)} file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
