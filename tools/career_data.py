"""Canonical labor-market figures for the notebooks' 💼 career sections.

WHY THIS FILE EXISTS
--------------------
Every number in a notebook's career section is a number that goes stale.
Median pay is restated by BLS each spring; ten-year projections get a new
base year every other year; the New York Fed's recent-graduate table moves
quarterly. Twelve notebooks with hand-typed figures would mean twelve
separate archaeology jobs every August.

So the figures live here once, with a source URL and an as-of date each,
and `--check` tells you which notebooks have drifted away from them.

ANNUAL UPDATE, roughly 20 minutes each August:
  1. Open each SOURCE url below, copy the current Quick Facts numbers in.
  2. Bump VERIFIED to today's date.
  3. Run `python tools/career_data.py --check` to see which notebooks
     still quote the old figures, and fix those cells.
  4. Run `python tools/career_data.py --render <key>` to get the markdown
     table for a cell, already formatted and footnoted.

A NOTE ON PRECISION
-------------------
BLS restates median pay to the dollar; that precision is real but invites
false confidence, so the notebooks round to the nearest thousand and always
print the as-of date beside it. The exact figure is kept here so the
rounding is checkable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Date the figures below were last confirmed against their sources.
VERIFIED = "2026-08-20"

# ---------------------------------------------------------------------------
# Whole-field context (Notebook 1). Sources: New York Fed, "The Labor Market
# for Recent College Graduates"; BLS Occupational Outlook Handbook overview.
# ---------------------------------------------------------------------------

MARKET = {
    "nyfed_url": "https://www.newyorkfed.org/research/college-labor-market",
    "as_of": "2026 Q2",
    # Recent graduates, ages 22-27, by major.
    "cs_unemployment": 6.1,
    "compeng_unemployment": 7.5,
    "all_grads_unemployment": 5.6,
    # "Underemployed" = working a job that does not require a degree.
    "cs_underemployment": 19.1,
    "all_grads_underemployment": 42.0,
}

# ---------------------------------------------------------------------------
# Per-role figures. `duties` are paraphrased from the BLS "What They Do"
# section — paraphrased, not quoted, so they can be written at the course's
# reading level without misrepresenting the source.
# ---------------------------------------------------------------------------

ROLES = {
    "infosec": {
        "notebook": "COMP1150_NB11_Cybersecurity",
        "title": "Information Security Analyst",
        "soc": "15-1212",
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm",
        "median_pay": 124_910,
        "pay_as_of": "May 2024",
        "outlook_pct": 29,
        "outlook_period": "2024-2034",
        "openings_per_year": 16_000,
        "entry_education": "Bachelor's degree, though BLS notes some enter with a high school diploma plus industry training and certifications",
        "duties": [
            "watch the organization's networks for breaches, and investigate the ones that happen",
            "install and maintain the defenses — firewalls, encryption",
            "look for weaknesses in systems before an attacker does",
            "write up what was attempted, what got through, and what it cost",
            "recommend fixes to management, and help staff use the new tools",
        ],
    },
    "software_dev": {
        "notebook": "COMP1150_NB04_ControlFlowFunctions",
        "title": "Software Developer",
        "soc": "15-1252",
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm",
        "median_pay": None,  # TODO confirm against source before publishing
        "pay_as_of": "May 2024",
        "outlook_pct": 15,
        "outlook_period": "2024-2034",
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "duties": [],
    },
    "data_scientist": {
        "notebook": "COMP1150_NB09_Databases",
        "title": "Data Scientist",
        "soc": "15-2051",
        "source": "https://www.bls.gov/ooh/math/data-scientists.htm",
        "median_pay": 112_590,
        "pay_as_of": "May 2024",
        "outlook_pct": 34,
        "outlook_period": "2024-2034",
        "openings_per_year": 23_400,
        "entry_education": "Bachelor's degree; some employers prefer a master's",
        "duties": [],
    },
    "web_dev": {
        "notebook": "COMP1150_NB10_OSNetworksWeb",
        "title": "Web Developer",
        "soc": "15-1254",
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/web-developers.htm",
        "median_pay": 90_930,
        "pay_as_of": "May 2024",
        "outlook_pct": 7,
        "outlook_period": "2024-2034",
        "openings_per_year": 14_500,
        "entry_education": "Varies — high school diploma through bachelor's degree",
        "duties": [],
    },
    "programmer": {
        # Included for contrast in Notebook 1, not as a role to aim at:
        # the title is shrinking while the work migrates into other titles.
        "notebook": "COMP1150_NB01_WhatIsComputing",
        "title": "Computer Programmer",
        "soc": "15-1251",
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/computer-programmers.htm",
        "median_pay": 98_670,
        "pay_as_of": "May 2024",
        "outlook_pct": -6,
        "outlook_period": "2024-2034",
        "openings_per_year": 5_500,
        "entry_education": "Bachelor's degree",
        "duties": [],
    },
    "systems_analyst": {
        "notebook": "COMP1150_NB08_SoftwareEngineering",
        "title": "Computer Systems Analyst",
        "soc": "15-1211",
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/computer-systems-analysts.htm",
        "median_pay": 105_850,
        "pay_as_of": "May 2025",
        "outlook_pct": 8,
        "outlook_period": "2025-2035",
        "openings_per_year": 32_900,
        "entry_education": "Bachelor's degree",
        "duties": [],
    },
}


def money(n: int | None) -> str:
    """Round to the nearest thousand — see the note on precision above."""
    return "—" if n is None else f"${round(n / 1000):,},000"


def render(key: str) -> str:
    """Emit the markdown table for one role's career cell."""
    r = ROLES[key]
    pct = f"+{r['outlook_pct']}%" if r["outlook_pct"] >= 0 else f"{r['outlook_pct']}%"
    openings = "—" if r["openings_per_year"] is None else f"about {r['openings_per_year']:,} a year"
    return (
        f"| | {r['title']} |\n|---|---|\n"
        f"| **Median pay** | {money(r['median_pay'])} ({r['pay_as_of']}) |\n"
        f"| **Projected change** | {pct}, {r['outlook_period']} |\n"
        f"| **Openings** | {openings} |\n"
        f"| **Typical entry education** | {r['entry_education']} |\n\n"
        f"*Source: U.S. Bureau of Labor Statistics, "
        f"[Occupational Outlook Handbook]({r['source']}), SOC {r['soc']}. "
        f"Figures retrieved {VERIFIED}.*"
    )


def incomplete() -> list[str]:
    """Roles still carrying a placeholder that must not be published."""
    return [k for k, r in ROLES.items() if r["median_pay"] is None]


def career_section(nb: dict) -> tuple[str, set[int]]:
    """Return the text of a notebook's 💼 career section, and its cell indices.

    The section is contiguous: it opens on the markdown cell whose heading
    carries 💼 and runs until the next `##` heading. Splitting the prose, the
    figures table, and the Think About It across separate cells is the house
    style, so a per-cell check would false-alarm on every one of them.
    """
    cells = nb["cells"]
    start = next(
        (i for i, c in enumerate(cells)
         if c["cell_type"] == "markdown" and "💼" in "".join(c["source"]).split("\n", 1)[0]),
        None,
    )
    if start is None:
        return "", set()
    idx = {start}
    for i in range(start + 1, len(cells)):
        src = "".join(cells[i]["source"])
        if cells[i]["cell_type"] == "markdown" and src.lstrip().startswith("## "):
            break
        idx.add(i)
    return "\n".join("".join(cells[i]["source"]) for i in sorted(idx)), idx


def check(repo_root: Path) -> int:
    """Report notebooks whose career sections have drifted from the figures here."""
    problems: list[str] = []

    for key in incomplete():
        problems.append(f"{key}: median_pay is a placeholder — confirm against {ROLES[key]['source']}")

    for key, r in ROLES.items():
        path = repo_root / "v2" / "notebooks" / f"{r['notebook']}.ipynb"
        if not path.exists():
            problems.append(f"{key}: no such notebook {r['notebook']}.ipynb")
            continue
        nb = json.loads(path.read_text(encoding="utf-8"))
        text, _ = career_section(nb)
        if not text:
            continue  # no career section yet — nothing to drift
        if r["median_pay"] is not None and money(r["median_pay"]) not in text:
            problems.append(
                f"{r['notebook']}: pay reads stale — expected {money(r['median_pay'])} ({r['pay_as_of']})"
            )
        pct = f"+{r['outlook_pct']}%" if r["outlook_pct"] >= 0 else f"{r['outlook_pct']}%"
        if pct not in text:
            problems.append(f"{r['notebook']}: outlook reads stale — expected {pct}")
        if VERIFIED not in text:
            problems.append(f"{r['notebook']}: 'retrieved' date is not {VERIFIED}")

    # Any bare four-digit dollar-thousands figure outside a career cell is
    # probably a number someone typed by hand and will forget to update.
    for path in sorted((repo_root / "v2" / "notebooks").glob("*.ipynb")):
        nb = json.loads(path.read_text(encoding="utf-8"))
        _, in_section = career_section(nb)
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] != "markdown" or i in in_section:
                continue
            for m in re.findall(r"\$\d{2,3},\d{3}", "".join(c["source"])):
                problems.append(f"{path.name} cell {i}: salary figure {m} outside the career section")

    if problems:
        print(f"career data: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"career data: all notebooks match figures verified {VERIFIED}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if any notebook has drifted")
    ap.add_argument("--render", metavar="ROLE", help=f"print a role's markdown table ({', '.join(ROLES)})")
    args = ap.parse_args()
    repo_root = Path(__file__).resolve().parent.parent

    if args.render:
        if args.render not in ROLES:
            print(f"unknown role {args.render!r}; known: {', '.join(ROLES)}", file=sys.stderr)
            return 2
        print(render(args.render))
        return 0
    if args.check:
        return check(repo_root)

    print(f"figures verified {VERIFIED}\n")
    for key, r in ROLES.items():
        flag = "  ⚠ placeholder" if r["median_pay"] is None else ""
        print(f"  {key:16} {r['title']:32} {money(r['median_pay']):>10}{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
