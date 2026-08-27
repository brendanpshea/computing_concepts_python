"""Canonical labor-market figures for the notebooks' 💼 career sections.

WHY THIS FILE EXISTS
--------------------
Every number in a career section is a number that goes stale. Median pay is
restated by BLS each spring; ten-year projections get a new base year every
other year; the New York Fed's recent-graduate table moves quarterly. Twelve
notebooks with hand-typed figures would mean twelve archaeology jobs each
August. So the figures live here once, and `--check` reports which notebooks
have drifted away from them.

CONFIDENCE
----------
Every figure carries a `confidence`:

  "confirmed"  — someone opened the SOURCE url and read it off the page.
  "secondhand" — taken from a search result quoting the page. Specific and
                 internally consistent, but not read off the source itself.
  "suspect"    — second-hand AND something about it does not add up. See the
                 note on the row.
  None value   — not established. `--check` fails while any remain.

Most rows below are "confirmed": read off the BLS Quick Facts tables by the
instructor on 2026-08-27, when the Bureau had rolled to the 2025-2035
projection round. Two rows are still on the superseded 2024-2034 round and
are marked "stale"; they are wrong until someone opens their page.

WHY THE BASE YEAR IS PRINTED EVERYWHERE
---------------------------------------
A BLS projection is a model run from a base year, not a measurement of now.
The 2025-2035 round replaced the 2024-2034 round in 2026, and it moved real
numbers: information security fell from +29% to +21%, software development
from +15% to +10%. A course that had hand-typed the old figures would still
be teaching them. So a notebook must never print "+10%" without printing
"2025-2035" beside it, and Notebook 1 teaches students why a projection and
a current unemployment rate can disagree.

ANNUAL UPDATE, roughly 20 minutes each August:
  1. Open each SOURCE url, copy the current Quick Facts numbers in, and set
     that row's confidence to "confirmed".
  2. Bump VERIFIED to today's date.
  3. `python tools/career_data.py --check` lists notebooks quoting old figures.
  4. `python tools/career_data.py --render <role>` prints the replacement table.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERIFIED = "2026-08-27"

# ---------------------------------------------------------------------------
# Whole-field context for Notebook 1's block.
# ---------------------------------------------------------------------------

MARKET = {
    "nyfed_url": "https://www.newyorkfed.org/research/college-labor-market",
    "as_of": "2026 Q2",
    "confidence": "secondhand",
    # Recent graduates, ages 22-27, by major.
    "cs_unemployment": 6.1,
    "compeng_unemployment": 7.5,
    "all_grads_unemployment": 5.6,
    # "Underemployed" = working a job that does not require a degree.
    "cs_underemployment": 19.1,
    "all_grads_underemployment": 42,
}

# ---------------------------------------------------------------------------
# CompTIA, "State of the Tech Workforce" (2026 release), analysing Lightcast
# and BLS data. A different lens from the OOH: it counts the whole tech
# workforce rather than occupation by occupation, and it publishes two things
# the OOH does not — wage percentiles, and replacement hiring.
#
# Attribution matters here. CompTIA reserves reproduction rights on the
# report, so notebooks cite individual figures with a source line and never
# reproduce its tables. Facts with attribution; not the layout.
# ---------------------------------------------------------------------------

COMPTIA = {
    "release": "2026",
    "title": "State of the Tech Workforce",
    "url": "https://www.comptia.org/",
    "confidence": "confirmed",

    # The whole tech workforce, and the year it went backwards.
    "net_tech_employment_2025": 9_597_888,
    "net_tech_change_2025": -33_624,          # -0.3% year over year
    "net_tech_pct_2025": -0.3,
    "net_tech_pct_2026_proj": 1.9,
    "tech_occupation_change_2025": 1_287,     # +0.02% — essentially flat
    "tech_occupation_2025": 5_931_208,

    # National tech-occupation wage percentiles (2024, most recent available).
    # CompTIA notes the 10th and 25th percentiles correspond to early-career
    # positions — which is the number a student should plan around, not the
    # median every salary article quotes.
    "wage_p10": 55_807,
    "wage_p25": 77_850,
    "wage_p50": 112_805,
    "wage_p75": 155_364,
    "wage_p90": 197_604,
    "wage_vs_national_median_pct": 126,

    # Replacement hiring, 2026-2036: the reason a shrinking occupation still
    # hires. Retirements plus people leaving the field, before any growth.
    "replacement_rate_pct": 6,
    "replacement_support_specialists": 42_915,
    "replacement_sysadmins": 15_083,
    "replacement_data_scientists": 15_317,
    "replacement_cybersecurity": 11_170,
    "replacement_software_devs": 90_587,

    # AI hiring. The headline is not the dedicated AI job; it is that AI
    # skills are being asked for most often at the *entry* level.
    "ai_skill_postings": 1_229_505,
    "ai_postings_0_3_years_pct": 35,
    "ai_postings_4_6_years_pct": 24,
    "ai_postings_7_plus_years_pct": 23,
    "dedicated_ai_title_growth_pct": 81,
    # Postings by skill category, largest to smallest — AI is the smallest.
    "skill_postings": {
        "Digital fluency": 14_029_916,
        "Infrastructure and support": 5_552_421,
        "Data analytics": 5_032_662,
        "Cybersecurity": 3_945_864,
        "AI": 1_229_505,
    },
}

# Minnesota, because this course is taught in Minnesota and a student in
# Rochester is not planning a career in San Jose.
MINNESOTA = {
    "net_tech_employment": 183_652,
    "net_tech_change_2025": -1_744,           # -0.9% year over year
    "tech_occupation_2025": 107_641,
    "tech_occupation_2026_proj": 108_452,     # +0.8%, below the 1.34% benchmark
    "wage_p10": 60_655,
    "wage_p25": 79_107,
    "wage_p50": 110_034,
    "wage_p75": 140_885,
    "wage_p90": 171_707,
    "wage_vs_state_median_pct": 107,
    "cost_of_living_index": 101.8,
    "confidence": "confirmed",
}

# ---------------------------------------------------------------------------
# Per-role figures.
#
# `median_pay` is either one number, or a dict when BLS reports one outlook
# for an occupation but separate wages for the tiers inside it (computer
# support and database work are both split this way). Splitting is not a
# formatting quirk — the gap between the tiers is often the gap between the
# job a student can get now and the one they can get in five years.
# ---------------------------------------------------------------------------

ROLES = {
    "support": {
        "notebook": 'COMP1150_NB02_MachineArchitecture',
        "title": 'Computer Support Specialist',
        "soc": '15-1231, 15-1232',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/computer-support-specialists.htm",
        "median_pay": 62_890,
        "pay_as_of": "2025",
        "outlook_pct": -3,
        "outlook_period": "2025-2035",
        "jobs": 903_100,
        "employment_change": -24_300,
        "openings_per_year": None,
        "entry_education": 'Varies — BLS points to its “How to Become One” section rather than naming one credential; network support typically wants an associate degree, user support some college, and either may be entered with a high school diploma plus IT certifications',
        "confidence": "confirmed",
    },
    "qa": {
        "notebook": 'COMP1150_NB03_PseudocodeFlowcharts',
        "title": 'QA Analyst & Tester',
        "soc": '15-1253',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm",
        "median_pay": 134_040,
        "pay_as_of": "2025",
        "outlook_pct": 10,
        "outlook_period": "2025-2035",
        "jobs": 1_905_400,
        "employment_change": 185_400,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "confidence": "confirmed",
        # BLS reports these on one page with one median in Quick Facts.
        "shared_outlook": 'software developers, QA analysts, and testers together',
        "shared_pay": True,
    },
    "software_dev": {
        "notebook": 'COMP1150_NB04_ControlFlowFunctions',
        "title": 'Software Developer',
        "soc": '15-1252',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm",
        "median_pay": 134_040,
        "pay_as_of": "2025",
        "outlook_pct": 10,
        "outlook_period": "2025-2035",
        "jobs": 1_905_400,
        "employment_change": 185_400,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "confidence": "confirmed",
        # BLS reports these on one page with one median in Quick Facts.
        "shared_outlook": 'software developers, QA analysts, and testers together',
        "shared_pay": True,
    },
    "systems_analyst": {
        "notebook": 'COMP1150_NB06_ModulesOOP',
        "title": 'Computer Systems Analyst',
        "soc": '15-1211',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/computer-systems-analysts.htm",
        "median_pay": 105_850,
        "pay_as_of": "2025",
        "outlook_pct": 8,
        "outlook_period": "2025-2035",
        "jobs": 544_400,
        "employment_change": 42_900,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "confidence": "confirmed",
    },
    "dba": {
        "notebook": 'COMP1150_NB09_Databases',
        "title": 'Database Administrator & Architect',
        "soc": '15-1242, 15-1243',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm",
        "median_pay": 126_760,
        "pay_as_of": "2025",
        "outlook_pct": 4,
        "outlook_period": "2025-2035",
        "jobs": 144_500,
        "employment_change": 6_500,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "confidence": "confirmed",
    },
    "infosec": {
        "notebook": 'COMP1150_NB11_Cybersecurity',
        "title": 'Information Security Analyst',
        "soc": '15-1212',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm",
        "median_pay": 129_180,
        "pay_as_of": "2025",
        "outlook_pct": 21,
        "outlook_period": "2025-2035",
        "jobs": 192_900,
        "employment_change": 40_600,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree, and BLS lists less than five years of related work experience",
        "confidence": "confirmed",
    },
    "programmer": {
        "notebook": None,
        "title": 'Computer Programmer',
        "soc": '15-1251',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/computer-programmers.htm",
        "median_pay": 100_390,
        "pay_as_of": "2025",
        "outlook_pct": -7,
        "outlook_period": "2025-2035",
        "jobs": 110_800,
        "employment_change": -8_100,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "confidence": "confirmed",
    },
    "web_dev": {
        "notebook": None,
        "title": 'Web Developer & Digital Designer',
        "soc": '15-1254, 15-1255',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/web-developers.htm",
        "median_pay": 99_520,
        "pay_as_of": "2025",
        "outlook_pct": 5,
        "outlook_period": "2025-2035",
        "jobs": 220_100,
        "employment_change": 11_300,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree",
        "confidence": "confirmed",
    },
    "network_architect": {
        "notebook": None,
        "title": 'Computer Network Architect',
        "soc": '15-1241',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/computer-network-architects.htm",
        "median_pay": 134_050,
        "pay_as_of": "2025",
        "outlook_pct": 8,
        "outlook_period": "2025-2035",
        "jobs": 181_800,
        "employment_change": 14_100,
        "openings_per_year": None,
        "entry_education": "Bachelor's degree, plus five years or more of related work experience",
        "confidence": "confirmed",
    },
    # Still on the superseded 2024-2034 round. Wrong until refreshed.
    "sysadmin": {
        "notebook": 'COMP1150_NB10_OSNetworksWeb',
        "title": 'Network & Computer Systems Administrator',
        "soc": '15-1244',
        "source": "https://www.bls.gov/ooh/computer-and-information-technology/network-and-computer-systems-administrators.htm",
        "median_pay": 96_800,
        "pay_as_of": "May 2024",
        "outlook_pct": -4,
        "outlook_period": "2024-2034",
        "jobs": None,
        "employment_change": None,
        "openings_per_year": 14_300,
        "entry_education": "Often a bachelor's degree; some positions take an associate degree or certification plus related experience",
        "confidence": "comptia",
        "note": ("BLS has not restated this occupation for the 2025-2035 round, so the "
                 "notebook uses CompTIA figures instead. Swap back when the OOH page updates."),
    },
    "data_scientist": {
        "notebook": 'COMP1150_NB12_AIMLEthics',
        "title": 'Data Scientist',
        "soc": '15-2051',
        "source": "https://www.bls.gov/ooh/math/data-scientists.htm",
        "median_pay": 112_590,
        "pay_as_of": "May 2024",
        "outlook_pct": 34,
        "outlook_period": "2024-2034",
        "jobs": None,
        "employment_change": None,
        "openings_per_year": 23_400,
        "entry_education": "Bachelor's degree; some employers prefer a master's",
        "confidence": "comptia",
        "note": ("BLS has not restated this occupation for the 2025-2035 round, so the "
                 "notebook uses CompTIA figures instead. Swap back when the OOH page updates."),
    },
}

# Notebooks whose 💼 block is about a process rather than one occupation, so
# `--check` knows not to expect figures from a role row.
PROCESS_BLOCKS = {
    "COMP1150_NB01_WhatIsComputing": "the shape of the field, and how to read a labor number",
    "COMP1150_NB05_CollectionsADTs": "reading a job posting that asks for more than you have",
    "COMP1150_NB07_SearchingSorting": "the technical interview",
    "COMP1150_NB08_SoftwareEngineering": "your first ninety days",
}


def money(n: int | None) -> str:
    return "—" if n is None else f"${round(n / 1000):,},000"


def pay_rows(r: dict) -> list[str]:
    """One table row for a single wage, or one per tier when BLS splits them.

    A tier whose figure is not yet established is left out of the table
    rather than printed as a dash — a visible hole in a student-facing
    table reads as sloppiness, and `--check` is already tracking the gap.
    """
    pay = r["median_pay"]
    if isinstance(pay, dict):
        return [f"| **Median pay — {tier.lower()}** | {money(v)} ({r['pay_as_of']}) |"
                for tier, v in pay.items() if v is not None]
    return [f"| **Median pay** | {money(pay)} ({r['pay_as_of']}) |"]


def render(key: str) -> str:
    r = ROLES[key]
    pct = f"+{r['outlook_pct']}%" if r["outlook_pct"] >= 0 else f"{r['outlook_pct']}%"
    lines = [f"| | {r['title']} |", "|---|---|", *pay_rows(r),
             f"| **Projected change** | {pct}, {r['outlook_period']} |"]
    if r.get("jobs"):
        chg = r["employment_change"]
        lines.append(f"| **Jobs in {r['pay_as_of']}** | {r['jobs']:,} |")
        lines.append(f"| **Change over the decade** | {chg:+,} |")
    elif r.get("openings_per_year"):
        lines.append(f"| **Openings** | about {r['openings_per_year']:,} a year |")
    lines.append(f"| **Typical entry education** | {r['entry_education']} |")

    base = r["outlook_period"].split("-")[0]
    footnote = (f"*Source: U.S. Bureau of Labor Statistics, "
                f"[Occupational Outlook Handbook]({r['source']}), SOC {r['soc']}. "
                f"Figures retrieved {VERIFIED}. The projection is a forecast made "
                f"from a {base} base year, not a measurement of today.*")
    if r.get("shared_outlook"):
        extra = (f" BLS reports the outlook, headcount and median pay for "
                 f"{r['shared_outlook']}.") if r.get("shared_pay") else \
                (f" BLS reports the outlook for {r['shared_outlook']}.")
        footnote = footnote[:-1] + extra + "*"
    return "\n".join(lines) + "\n\n" + footnote


def missing() -> list[str]:
    out = []
    for k, r in ROLES.items():
        pay = r["median_pay"]
        if pay is None:
            out.append(f"{k}: median_pay not established")
        elif isinstance(pay, dict):
            out += [f"{k}: median_pay[{t!r}] not established" for t, v in pay.items() if v is None]
    return out


def career_section(nb: dict) -> tuple[str, set[int]]:
    """Text and cell indices of a notebook's 💼 section.

    The section is contiguous: it opens on the markdown cell whose heading
    carries 💼 and runs to the next `##` heading. Prose, figures table and
    Think About It live in separate cells, so a per-cell check would false
    alarm on every one of them.
    """
    cells = nb["cells"]
    start = next((i for i, c in enumerate(cells)
                  if c["cell_type"] == "markdown"
                  and "💼" in "".join(c["source"]).split("\n", 1)[0]), None)
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
    problems: list[str] = []
    warnings: list[str] = []
    problems += missing()

    nb_dir = repo_root / "v2" / "notebooks"
    for key_, r in ROLES.items():
        key = key_
        if r["notebook"] is None:
            continue
        path = nb_dir / f"{r['notebook']}.ipynb"
        if not path.exists():
            problems.append(f"{key}: no such notebook {r['notebook']}.ipynb")
            continue
        text, _ = career_section(json.loads(path.read_text(encoding="utf-8")))
        if not text:
            warnings.append(f"{r['notebook']}: no 💼 section yet ({r['title']})")
            continue
        if r.get("confidence") == "comptia":
            # The notebook quotes CompTIA here; check that instead of BLS.
            key = {"sysadmin": "replacement_sysadmins",
                   "data_scientist": "replacement_data_scientists"}.get(key_)
            if key and f"{COMPTIA[key]:,}" not in text:
                problems.append(f"{r['notebook']}: CompTIA replacement figure reads stale")
            if "CompTIA" not in text:
                problems.append(f"{r['notebook']}: CompTIA figures used but not attributed")
            continue
        pay = r["median_pay"]
        for v in (pay.values() if isinstance(pay, dict) else [pay]):
            if v is not None and money(v) not in text:
                problems.append(f"{r['notebook']}: pay reads stale — expected {money(v)}")
        pct = f"+{r['outlook_pct']}%" if r["outlook_pct"] >= 0 else f"{r['outlook_pct']}%"
        if pct not in text:
            problems.append(f"{r['notebook']}: outlook reads stale — expected {pct}")
        if r["outlook_period"] not in text:
            problems.append(f"{r['notebook']}: base year missing — every projection needs {r['outlook_period']} beside it")
        if VERIFIED not in text:
            problems.append(f"{r['notebook']}: 'retrieved' date is not {VERIFIED}")

    nb1 = nb_dir / "COMP1150_NB01_WhatIsComputing.ipynb"
    if nb1.exists():
        text, _ = career_section(json.loads(nb1.read_text(encoding="utf-8")))
        if text:
            for field in ("cs_unemployment", "all_grads_unemployment",
                          "cs_underemployment", "all_grads_underemployment"):
                if f"{MARKET[field]}%" not in text:
                    problems.append(
                        f"COMP1150_NB01_WhatIsComputing: {field} reads stale — expected {MARKET[field]}%")
            if MARKET["as_of"] not in text:
                problems.append(
                    f"COMP1150_NB01_WhatIsComputing: market as-of is not {MARKET['as_of']}")

    for stem, topic in PROCESS_BLOCKS.items():
        path = nb_dir / f"{stem}.ipynb"
        if path.exists():
            text, _ = career_section(json.loads(path.read_text(encoding="utf-8")))
            if not text:
                warnings.append(f"{stem}: no 💼 section yet ({topic})")

    # A salary figure loose in the notebook is one nobody will remember to update.
    for path in sorted(nb_dir.glob("*.ipynb")):
        nb = json.loads(path.read_text(encoding="utf-8"))
        _, in_section = career_section(nb)
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] != "markdown" or i in in_section:
                continue
            for m in re.findall(r"\$\d{2,3},\d{3}", "".join(c["source"])):
                problems.append(f"{path.name} cell {i}: salary figure {m} outside the career section")

    unconfirmed = [k for k, r in ROLES.items() if r.get("confidence") == "secondhand"]
    suspect = [k for k, r in ROLES.items() if r.get("confidence") in ("suspect", "stale")]
    borrowed = [k for k, r in ROLES.items() if r.get("confidence") == "comptia"]

    for w in warnings:
        print(f"  · {w}")
    if warnings:
        print()
    if problems:
        print(f"career data: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  - {p}")
    else:
        print(f"career data: notebooks match the figures verified {VERIFIED}")

    if unconfirmed:
        print(f"\n  {len(unconfirmed)} row(s) not yet read off the source — click through, then set")
        print(f"  confidence='confirmed': {', '.join(unconfirmed)}")
    if not unconfirmed and not suspect:
        print("\n  every row read off its source.")
    for k in suspect:
        print(f"\n  ⚠ {k}: {ROLES[k]['note']}\n    {ROLES[k]['source']}")
    for k in borrowed:
        print(f"\n  · {k}: using CompTIA figures — {ROLES[k]['source']}")

    return 1 if problems else 0


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
        pay = r["median_pay"]
        shown = (" / ".join(money(v) for v in pay.values()) if isinstance(pay, dict) else money(pay))
        pct = f"+{r['outlook_pct']}%" if r["outlook_pct"] >= 0 else f"{r['outlook_pct']}%"
        mark = {"confirmed": "", "stale": " ⚠ stale round", "suspect": " ⚠",
                "comptia": " · CompTIA"}.get(r.get("confidence"), " ·")
        print(f"  {key:16} {r['title']:42} {shown:>21}  {pct:>5}{mark}")
    print("\n  ⚠ needs refreshing — see the row's note")
    return 0


if __name__ == "__main__":
    sys.exit(main())
