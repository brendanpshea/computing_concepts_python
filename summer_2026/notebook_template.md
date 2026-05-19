# Notebook Template & Style Guide — Summer 2026

A template and authoring guide for the 12 main notebooks in the redesigned COMP 1150. Use this as a checklist when drafting; deviate when a topic demands it, but aim to keep the look and rhythm consistent across the semester.

---

## Targets at a Glance

| Spec | Target |
|------|--------|
| Total cells | ~45 |
| Word count (prose only) | ~6,000 |
| Reading level | 10th–12th grade |
| Exercises | 3–4, no inline solutions |
| AI-assisted exercise | At least 1, explicitly called out |
| Max code cell length | ~25 lines (split longer ones) |
| Max prose cell length | ~300 words (easier to project and read) |
| Primary graphics libraries | graphviz, matplotlib |

---

## Voice & Style

- **Reading level: 10th–12th grade.** Short sentences. Active voice. Plain words. Explain every technical term on first use and add it to the Key Terms glossary.
- **Concrete over abstract.** Every concept lands in a scene with named characters doing something recognizable. No abstract "a user" or "a programmer" — always Dwight, always Elizabeth Bennet, always Gandalf.
- **Funny when it fits; never forced.** The characters supply the humor. You don't need to punch up every paragraph.
- **Don't assume prior programming background.** A student can have seen zero code and still follow along.
- **Philosophical asides belong in the case studies, not the notebooks.** Notebooks are for doing. Case studies are for reflecting.

---
## Cast Balance & Representation

- **Every notebook world must include at least one named female character in a meaningful role.** She should do real conceptual work in the examples — making decisions, spotting errors, designing systems, asking good questions, or leading part of the scenario.
- **Avoid token casting.** Don't add one woman to the cast and then give all the technical action to male characters. Spread agency across the notebook.
- **Use role-fit, not stereotype.** Female characters can be leads, engineers, analysts, founders, operators, security specialists, or skeptics. Do not default them to only support or administrative roles unless that is being deliberately subverted.
- **Exercises should reflect this too.** At least one exercise prompt in each notebook should be framed around a female character's task, question, or problem.
- **When adapting a source world with fewer well-known women, elevate the women who are present or use adjacent canonical characters where appropriate.** Keep the casting recognizable, but prioritize balance.

### Quick casting check
Before drafting a notebook, confirm:
- at least one female character appears in the opening hook
- at least one female character appears in examples or code variable names
- at least one exercise is assigned by or centered on a female character
- female characters have technical or decision-making roles, not just reaction roles
## The Cast Convention

**Pick one "world" per notebook.** Keep the cast consistent inside a notebook so students build a mental model of who's who. Switch worlds between notebooks for variety.

**Within a world, spread characters across several different businesses and industries.** A single "world = one company" setup makes every code example rhyme with the last one. Instead, cast the source-material characters across a *universe* of 5–6 small-to-mid-sized businesses — a clinic here, a game studio there, a logistics firm, a lending shop, a civic agency. This is what gives the course its code variety: a dictionary example in the Austen world can come from Elizabeth's publishing house, while a list example can come from Jane's clinic and a class example can come from Darcy's investment fund.

Each roster below aims for:
- **5–6 named characters spread across 5–6 distinct businesses** (healthcare, finance, logistics, retail, media, game design, civic tech, security, ag, manufacturing, etc.)
- **Even gender balance** — at least 3F/3M in every roster of 6
- **Role-fit, not stereotype** — female characters lead, build, investigate, and engineer; they are not defaulted into support roles

Each business gets a "code territory" note — the kinds of code examples that industry naturally produces. Use this to pick the right business for the concept you're teaching.

---

### NB 1 — Sherlock Holmes (Victorian-Modern London)
*Pairs with: What Is Computing? + AI Pair-Programmer.*

| Business | Character (role) | Code territory |
|---|---|---|
| 221B Consulting (forensic data firm) | **Sherlock Holmes**, lead analyst | log parsing, pattern matching, evidence chains, set operations |
| Adler Intelligence (private intel) | **Irene Adler**, founder & CEO | risk scoring, encrypted records, access control |
| Watson Family Practice (GP clinic) | **John Watson**, physician-owner | patient records, scheduling, symptom dictionaries |
| Hudson Holdings (property management) | **Mrs. Hudson**, owner | tenant ledgers, rent tracking, maintenance tickets |
| Lestrade Public Safety Tech (civic software) | **Inspector Lestrade**, director | incident reports, mapping, open government data |
| Hunter Tutoring (exam prep & mentoring) | **Violet Hunter**, founder | student progress, test scores, cohort scheduling |

**Balance:** 3F / 3M.

---

### NB 2 — Classic Nintendo (The Mushroom Kingdom & Neighbors)
*Pairs with: Machine Architecture & Data Representation. Retro-hardware feel is a natural fit.*

| Business | Character (role) | Code territory |
|---|---|---|
| Peach's Castle Events (event management platform) | **Princess Peach**, founder | guest lists, RSVP tables, seat assignments |
| Samus Galactic Security (contract security) | **Samus Aran**, founder-engineer | sensor data, bit flags, armor-upgrade systems |
| Rosalina Observatory (astronomy research lab) | **Rosalina**, principal investigator | telescope data, binary encoding, fixed-point math |
| Mario Bros. Construction (building & repair) | **Mario**, owner-operator | parts inventory, job scheduling, blueprints |
| Luigi's Ghost-Hunting Services (paranormal-tech) | **Luigi**, lead technician | sensor readings, error handling, bit masks |
| Bowser Entertainment (rival theme-park chain) | **Bowser**, CEO | ride throughput, queue data, ticketing |

**Balance:** 3F / 3M.

---

### NB 3 — Dickens (Victorian-Modern England)
*Pairs with: Python Basics via Pseudocode & Flowcharts. Dickens's clerks and ledgers map beautifully to methodical code.*

| Business | Character (role) | Code territory |
|---|---|---|
| Scrooge & Marley Accounting | **Ebenezer Scrooge**, managing partner | ledgers, totals, tax calculations, pseudocode for billing |
| Havisham Bridal Emporium (legacy retail) | **Miss Havisham**, owner | inventory, price lookups, loyalty records |
| Dombey Shipping (logistics & freight) | **Florence Dombey**, operations director | cargo manifests, route planning, delivery status |
| Wilfer Data Services (small data consultancy) | **Bella Wilfer**, analyst-founder | CSV parsing, summary stats, flowcharts |
| Cratchit Bookkeeping (small-business accounting) | **Bob Cratchit**, sole proprietor | invoices, overdue accounts, rate calculations |
| Nickleby Tutoring (adult literacy) | **Kate Nickleby**, co-founder | student records, lesson plans, progress flags |

**Balance:** 3F / 3M.

---

### NB 4 — Princess Bride (Florin & Guilder, Present Day)
*Pairs with: Control Flow & Problem Decomposition. Branching adventure maps to if/else.*

| Business | Character (role) | Code territory |
|---|---|---|
| Buttercup Ventures (adventure-tourism ops) | **Buttercup**, CEO | trip bookings, route branching, risk decisions |
| Valerie Community Pharmacy | **Valerie**, pharmacist-owner | prescription logic, dosing rules, refill triggers |
| Inigo Fencing Academy (martial-arts training) | **Inigo Montoya**, head instructor | class rosters, skill progression, practice loops |
| Fezzik Moving & Logistics | **Fezzik**, owner | truck loads, route decisions, weight limits |
| Max & Mabel Miracle Pharmacy (alt-medicine) | **Mabel** (Max's wife, re-cast from "Valerie") / **Miracle Max**, co-owners | batch processes, recipe loops, error handling |
| Queen's Governance Office (civic admin) | **Queen Bella**, chief of staff | permits, approvals, branching workflows |

**Balance:** 3F / 3M. *(Princess Bride has fewer named women; we elevate Queen Bella and split the pharmacy between Max and Mabel.)*

---

### NB 5 — Dunder Mifflin Universe (The Office)
*Pairs with: Collections & ADTs. The show's real-world side-businesses give us the variety we need.*

| Business | Character (role) | Code territory |
|---|---|---|
| Dunder Mifflin Scranton (paper sales) | **Pam Beesly**, office administrator | customer list, call logs, orders |
| Schrute Farms Agritourism | **Dwight Schrute**, proprietor | beet inventory, guest bookings, crop rotations |
| Kapoor Kareer Academy (professional development) | **Kelly Kapoor**, CEO | enrollments, cohorts, certification tracks |
| Vance Refrigeration | **Phyllis Vance** (partner, ops), Bob Vance (sales) | service tickets, unit inventory, route scheduling |
| Michael Scott Paper Co. (scrappy startup phase) | **Michael Scott**, founder | lean customer records, daily sales, discounts |
| Athlead Sports Marketing | **Jim Halpert**, co-founder | athlete portfolios, deal pipelines, event calendars |

**Balance:** 3F / 3M (Pam, Kelly, Phyllis / Dwight, Michael, Jim).

---

### NB 6 — Tolkien (Middle-earth, Modernized)
*Pairs with: Functions, Modules & OOP. Races, fellowships, and guilds = a natural OOP universe.*

| Business | Character (role) | Code territory |
|---|---|---|
| Lothlórien Research Institute (academic lab) | **Galadriel**, director | datasets, class hierarchies, research modules |
| Rohan Security Services (private security) | **Éowyn**, CEO | patrol schedules, incident classes, inheritance (Guard → Ranger) |
| Rivendell Library Systems (knowledge management) | **Arwen**, chief librarian | catalog objects, tag systems, document classes |
| Istari Advisory (management consulting) | **Gandalf**, senior partner | client records, advisory modules, reusable playbooks |
| Shire Logistics (last-mile delivery) | **Frodo Baggins**, junior operations engineer | package objects, route classes, courier methods |
| Erebor Mining & Materials | **Thorin Oakenshield**, managing director | extraction logs, ore-class hierarchies, shift scheduling |

**Balance:** 3F / 3M.

---

### NB 7 — Dr. Who (Multi-Era London, Time-Adjusted)
*Pairs with: Algorithms & Limits of Computation. Computability + paradoxes fit the Whoniverse.*

| Business | Character (role) | Code territory |
|---|---|---|
| TARDIS Travel (experimental travel platform) | **The Doctor** (13th, Jodie Whittaker era), founder | search over large graphs, route optimization |
| Song Archaeological Data (research & archives) | **River Song**, principal | indexing, search algorithms, text corpora |
| Martha Jones Telemedicine (remote clinic) | **Martha Jones**, medical director | triage algorithms, priority queues, diagnostic trees |
| UNIT Cybersecurity Division | **Kate Lethbridge-Stewart**, commanding officer | threat-detection algorithms, classification, Big O on log search |
| Torchwood Paranormal Research | **Captain Jack Harkness**, director | event timelines, halting-problem analogies |
| Mickey Smith Mechanics (garage + diagnostics) | **Mickey Smith**, owner | fault-finding algorithms, cost-of-repair decisioning |

**Balance:** 3F / 3M.

---

### NB 8 — Star Trek (Federation, Modernized)
*Pairs with: Software Engineering, Git & AI-Assisted Dev. Crew coordination + logs is a gift.*

| Business | Character (role) | Code territory |
|---|---|---|
| Voyager Research (academic-industry lab) | **Captain Janeway**, director | project planning, sprint backlogs, peer review |
| Seven of Nine Optimization (efficiency consulting) | **Seven of Nine**, principal | code reviews, refactoring examples, AI-assisted audits |
| Uhura Communications (networking & comms) | **Nyota Uhura**, CTO | version history, branch diagrams, release notes |
| Enterprise Engineering (systems integration) | **Captain Picard**, managing partner | requirements docs, architecture decisions |
| Data Analytics Group (ML engineering) | **Commander Data**, lead engineer | CI pipelines, automated tests, spec-to-code workflows |
| La Forge Infrastructure (devops & SRE) | **Geordi La Forge**, founder | deployments, rollbacks, incident postmortems |

**Balance:** 3F / 3M (Janeway, Seven, Uhura / Picard, Data, Geordi).

---

### NB 9 — Austen (Regency-Modern England)
*Pairs with: Databases (Relational & Non-Relational). Social networks = relational data.*

| Business | Character (role) | Code territory |
|---|---|---|
| Longbourn Publishing (independent press) | **Elizabeth Bennet**, editorial director | manuscripts, authors, royalties — classic relational data |
| Netherfield Community Health (clinic) | **Jane Bennet**, clinical director | patients, visits, prescriptions — joins + integrity constraints |
| Highbury Match (matchmaking app) | **Emma Woodhouse**, founder | profiles, compatibility tables — relational + document-store tradeoffs |
| Pemberley Capital (wealth management) | **Fitzwilliam Darcy**, CFO | accounts, transactions — normalization, indexing |
| Donwell Agricultural Systems (farm software) | **George Knightley**, co-founder | crop plots, yields, weather — time-series data |
| Delaford Veterans Services (nonprofit) | **Colonel Brandon**, executive director | clients, services, case files — mixed structured/unstructured |

**Balance:** 3F / 3M.

---

### NB 10 — Classic Crime Films (Modernized Metro Area)
*Pairs with: OS, Networks, Cloud & Web. Coordination + comms + heists naturally invoke networks.*

| Business | Character (role) | Code territory |
|---|---|---|
| Corleone Imports (specialty foods distribution) | **Michael Corleone**, COO | inventory nodes, distribution networks, supply chains |
| Connie Corleone Compliance (governance consulting) | **Connie Corleone**, managing partner | audit trails, access logs, policy engines |
| Adams & Hagen Legal (corporate law) | **Kay Adams**, partner / **Tom Hagen**, partner | case management, document APIs, client portals |
| Hill & Hill Realty | **Karen Hill**, broker-owner | listings API, location data, geo queries |
| McCauley Security Group (private security) | **Neil McCauley**, founder | access control, network monitoring, cloud logs |
| Eady Fine Art Advisory | **Eady**, principal | catalog APIs, provenance records, auction data |

**Balance:** 3F / 3M.

---

### NB 11 — Classic Horror (Gothic-Modern Europe)
*Pairs with: Cybersecurity & Secure Software Development. Monsters = threats, defenders = defenses.*

| Business | Character (role) | Code territory |
|---|---|---|
| Harker Risk & Insurance | **Mina Harker**, chief risk officer | threat modeling, risk scoring, breach reporting |
| Lavenza Ethics Advisory (responsible biotech consulting) | **Elizabeth Lavenza**, principal | policy enforcement, consent records, audit logs |
| Daaé Talent Management (performing arts) | **Christine Daaé**, founder | identity verification, stalker/abuse prevention, safe-list systems |
| Frankenstein BioLab (experimental biotech) | **Victor Frankenstein**, CTO | secure labs, access credentials, lab-notebook integrity |
| Van Helsing Threat Research | **Abraham Van Helsing**, director | intrusion detection, signature matching, incident response |
| Harker & Co. Legal (estate and security law) | **Jonathan Harker**, partner | secrets handling, document classification, contract review |

**Balance:** 3F / 3M.

---

### NB 12 — Classic Comic Books (Modern-Day Metro)
*Pairs with: AI, ML & Ethics. Power and responsibility, by design.*

| Business | Character (role) | Code territory |
|---|---|---|
| Themyscira Ethics Council (AI ethics nonprofit) | **Diana Prince**, executive director | bias audits, fairness metrics, policy frameworks |
| Oracle Cybersecurity (threat intel + ML) | **Barbara Gordon**, founder | anomaly detection, adversarial ML |
| Wakandan AI Research | **Shuri**, director of research | model training, dataset curation, evaluation |
| Stark AI Labs (applied ML products) | **Tony Stark**, CEO | LLM integrations, feature engineering |
| Daily Bugle Visual Intelligence (image ML) | **Peter Parker**, staff photographer / ML engineer | image classification, labeling pipelines |
| Wayne Research (long-horizon R&D) | **Bruce Wayne**, principal | forecasting models, simulation, "what could go wrong" studies |

**Balance:** 3F / 3M.

---

### Bench Worlds (swap in if a primary world doesn't fit)

These aren't in the rotation but are fully workable. Same rules apply: 5–6 businesses, 3F/3M minimum.

- **Shakespeare (Elizabethan-Modern Europe)** — Verona Ventures (Juliet, VC), Elsinore Media (Ophelia, exec producer; Hamlet, PM), Dunsinane Defense (Lady Macbeth, strategy), Portia Legal (Portia, partner), Illyria Weddings (Viola, founder), Cyprus Cyber (Othello, CISO).
- **Star Wars** — Rebel Ops Foundation (Leia), Jakku Salvage (Rey), Millennium Freight (Han Solo), Naboo Diplomatic Services (Padmé), Mandalorian Security (Bo-Katan), Jedi Archives (Ahsoka).
- **Grimm's Fairytales** — Red Delivery (Red Riding Hood), Cinderella Fulfillment (Cinderella), Rapunzel Wellness (Rapunzel), Hansel & Gretel Baking (Hansel), Rumpelstiltskin Lending (Rumpelstiltskin), Bremen Town Music (Bremen animals as label).
- **Wonderland / Oz** — Wonderland Tea Co. (Hatter), Oz Emerald Platform (Glinda), Kansas Farm Analytics (Dorothy), Alice Analytics (Alice), Tin Man Manufacturing (Tin Man), Scarecrow Ag-AI (Scarecrow).

---

**One world per notebook, 12 notebooks, 12 worlds.** Within each notebook, pick 3–5 of the 6 businesses based on what your concept sections need — you don't have to use every business in every notebook.

---

## Cell-by-Cell Skeleton

This is the recommended structure. The cell counts in parentheses are targets — adjust as the material requires.

### 1. Title banner (1 cell, markdown)
```markdown
# Notebook N: [Title]
### COMP 1150 — Computer Science Concepts
**Brendan Shea, PhD**
```
Attribution is to **Brendan Shea, PhD** — never the college. The course is *offered at* RCTC, but the notebooks are the author's copyrighted work.

### 2. Lecture video placeholder (1 cell, markdown)
```markdown
<!-- Lecture video link to be added -->
📺 **Lecture video:** *(coming soon)*
```

### 3. Learning Outcomes (1 cell, markdown)
```markdown
## Learning Outcomes

By the end of this notebook, you will be able to:
- [outcome 1, starting with a verb — Explain, Apply, Build, Distinguish, etc.]
- [outcome 2]
- [outcome 3]
- [outcome 4]

*Maps to course LOs: #, #, #*
```

### 4. Opening hook (2–3 cells, markdown)
Set the scene. Introduce the world and the cast you'll use throughout. State the question or problem the notebook will answer.

Keep this punchy — students decide in 30 seconds whether they're engaged.

### 5–40. Concept sections (4–5 sections, ~7 cells each)

Each concept section follows this pattern:

1. **Section heading** — `### [Section title]` (markdown, 1 cell)
2. **Concept intro** — why this matters, in plain words (markdown, 1 cell, ~150 words)
3. **Character-grounded example** — a scenario from the cast (markdown, 1 cell, ~150 words)
4. **Small code cell** — the minimal code needed to show the concept (code, 5–15 lines)
5. **Prose explanation** — what the code did and why (markdown, 1 cell, ~100 words)
6. **Variation or edge case** — another small code cell OR a matplotlib/graphviz diagram (code, 5–15 lines)
7. **Prose closer** — takeaway + transition to next section (markdown, 1 cell, ~75 words)

Not every section needs all seven cells. Some concepts are prose-only (e.g., a networking idea with a single diagram); some are code-heavy. Aim for the average.

### 41. Exercise block (3–4 exercises, each 1 cell). Can be interleaved through Content.
Each exercise in its own markdown cell, no solution cells in the notebook.
- Frame each as a task one of the cast asks the student to do
- Number them
- Mark at least one as `🤖 **AI-Assisted Exercise**` with an explicit instruction to use Gemini / Claude / ChatGPT and verify the result

Example exercise framing:
```markdown
### Exercise 3 — Dwight's Beet Inventory 🤖 AI-Assisted

Dwight wants a function that takes his beet-type dictionary and returns the three beet types with the lowest stock. Use Gemini to draft the function, then:

1. Paste the function into a code cell and run it against `dwights_beets` (defined above).
2. Find at least one thing the AI got wrong or could improve. Fix it.
3. In a markdown cell, write 2–3 sentences explaining what you changed and why.
```

### 42. Key Terms glossary (1–2 cells, markdown)
Alphabetical list of the technical terms introduced in the notebook. Each entry: term in bold, one-sentence plain-language definition.

```markdown
## Key Terms

- **Dictionary** — A collection that stores data as key-value pairs, where each key maps to one value.
- **Key** — The label you use to look up a value in a dictionary. Must be unique within a given dictionary.
- **Value** — The data stored under a key in a dictionary. Can be any type.
```

### 43. Summary (1 cell, markdown)
3–5 sentences recapping the main ideas. Not a full restatement — a "what should stick" note.

### 44. What's Next (1 cell, markdown)
1–2 sentences bridging to the next notebook. What problem is left open? What will we build on?

### 45. Credits / License (1 cell, markdown)
Standard footer, identical across all notebooks. Copyright is **Brendan Shea's**, not the college's:

```markdown
---
*COMP 1150 — Computer Science Concepts · Brendan Shea, PhD*  
*Content licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
```

Do not attribute the notebooks to Rochester Community and Technical College anywhere — title, footer, or body.

---

## Code Cell Conventions

**Default style (C): interleaved micro-cells with prose between.** Best for teaching a new idea step by step.

```
[code cell: create an empty dict]
[prose cell: explain what a dict is]
[code cell: add a key-value pair]
[prose cell: explain the syntax]
[code cell: access the value by key]
[prose cell: explain lookups]
```

**Fallback style (B): one clean block with framing prose.** Use when the code is irreducible (a class definition, a multi-step algorithm) and splitting it would hide the shape.

```
[prose cell: "The class below models a beet farm. It has three methods: ..."]
[code cell: the full class, 20-ish lines]
[prose cell: walk through what each method does]
```

**Rules regardless of style:**
- Never exceed ~25 lines in a single code cell.
- Use inline comments sparingly — one or two per cell at most. Prose cells carry the explanation.
- Every code cell should be runnable on its own or have its dependencies in the cell immediately above. Students will run cells out of order; plan for it.
- Name variables after characters when it reinforces the example (`dwights_beets`, not `d1`).

---

## Graphics Conventions

- **graphviz** — for structural relationships: flowcharts, class hierarchies, ER diagrams, network topologies, process trees, decision trees.
- **matplotlib** — for data, results, and comparisons: bar charts, line plots, scatter plots, histograms, timing comparisons for Big O.
- **PIL / ipywidgets** — sparingly, for bespoke visual demos.
- **All graphics are generated by code in the notebook.** No pasted-in images. This lets students tinker and see how the visual was built.
- **Label everything.** Every axis, every node, every legend entry. A diagram without labels is wasted cells.

---

## Cell-Size Discipline (for Reading & Projection)

- **Markdown cells:** aim for ~150 words, cap at ~300. If a cell is longer than a projector screen of readable text, split it.
- **Code cells:** 5–15 lines is the sweet spot. Hard cap ~25.
- **When in doubt, split.** A notebook with 50 short cells reads better than one with 30 dense cells.

---

## Slide-View Rhythm (mandatory for every code & figure cell)

These notebooks are presented one cell at a time. A code cell or figure that appears with no setup, or is immediately followed by a new section header, reads as a "cold" slide — the audience sees code/output with no idea why. **Never let a code or figure cell stand alone.** Every one gets sandwiched:

1. **Setup slide (markdown, before):** a `###` header + 1–2 sentences saying *what's about to appear and why*. The last sentence should point at the cell ("the next cell…", "the diagram below…").
2. **The code or figure cell.**
3. **Payoff slide (markdown, after):** a short explanation. For code use `### Understanding the Code` (bulleted, the new ideas only). For a graphviz/matplotlib figure use a one-line **`**Reading it:**`** caption that says how to read the picture.

Rules:

- This applies to **figures too**, not just code. A graphviz/matplotlib cell with no caption after it is the most common offender — fix it with a `**Reading it:**` line.
- A section intro can serve as the setup slide *only if* its final sentence explicitly points at the cell that follows. Otherwise add a dedicated setup slide.
- Keep both framing slides light (1–3 sentences). The goal is pacing, not padding — each should change what the reader knows.
- In slide view the pattern should always read: **setup → artifact → takeaway**, three readable slides, no orphaned code or uncaptioned diagrams.

---

## A Mini Worked Example

Below is a fragment of what a **dictionaries** section in NB 5 could look like, using Dunder Mifflin as the world. This is the model for voice and rhythm.

---

**[markdown cell]**

### Dictionaries: Looking Things Up Fast

Dwight has a problem. He keeps every beet farm record on sticky notes taped to his monitor, and whenever Pam asks for the price of Detroit Dark Red beets, he spends ten minutes rifling through paper. There has to be a better way.

A **dictionary** is Python's answer to Dwight's sticky notes. Instead of searching through a list one item at a time, a dictionary lets you look up a value instantly by its label — or **key**. If Dwight knows the beet name, he can get the price in a single step.

---

**[code cell]**

```python
dwights_beets = {
    "Detroit Dark Red": 2.50,
    "Chioggia": 3.10,
    "Golden": 2.75,
}
```

---

**[markdown cell]**

This creates a dictionary with three entries. On the left of each colon is a **key** (the beet name). On the right is the **value** (the price per pound). The whole thing is wrapped in curly braces.

---

**[code cell]**

```python
print(dwights_beets["Chioggia"])
```

---

**[markdown cell]**

When Dwight wants the price of Chioggia beets, he looks it up by key. Python jumps straight to that entry — it doesn't scan the other beets. That's the whole point of a dictionary: **fast lookup by name, not by position.**

---

**[code cell]**

```python
dwights_beets["Bull's Blood"] = 3.40
print(dwights_beets)
```

---

**[markdown cell]**

Adding a new beet is just as easy: assign a value to a new key. If Dwight ever wanted to update an existing price (say, Chioggia goes on sale), he'd use the same syntax — Python overwrites the existing value.

---

That's the rhythm. Short cells, a named character with a real-feeling problem, code that's small enough to read at a glance, and prose that explains what just happened in plain English.

---

## Checklist Before Publishing a Notebook

- [ ] Title, LOs, lecture-link placeholder, opening hook all present
- [ ] Cast is consistent throughout and comes from the planned world for this notebook
- [ ] 4–5 concept sections, each following the 7-cell pattern (or a defensible variation)
- [ ] 3–4 exercises, no inline solutions, at least one marked AI-Assisted
- [ ] Key Terms glossary covers every bolded term in the notebook
- [ ] Summary + What's Next + credits footer in place
- [ ] No code cell exceeds ~25 lines
- [ ] No prose cell exceeds ~300 words
- [ ] All graphics generated by code, all labeled
- [ ] **Slide-view rhythm:** every code & figure cell has a setup slide before and a payoff/`**Reading it:**` slide after — no cold or uncaptioned cells
- [ ] Word count ~6,000; cell count ~45
- [ ] Read through at projector resolution — no cell overflows a screen

---

## World Rotation for the 12 Notebooks (Draft)

A suggested rotation so no world repeats and the vibe varies session to session. Swap freely.

| NB | Topic | Proposed World |
|----|-------|----------------|
| 1 | What Is Computing? + AI Pair-Programmer | Sherlock Holmes (investigation + reasoning) |
| 2 | Machine Architecture & Data Representation | Classic Nintendo (NES hardware era feel) |
| 3 | Python via Pseudocode & Flowcharts | Dickens (clerks, ledgers, methodical work) |
| 4 | Control Flow & Decomposition | Princess Bride (if/else adventure branching) |
| 5 | Collections & ADTs | The Office / Dunder Mifflin |
| 6 | Functions, Modules & OOP | Tolkien (fellowship = module, races = classes) |
| 7 | Algorithms & Limits of Computation | Dr. Who (computability + time paradoxes) |
| 8 | Software Engineering, Git & AI-Assisted Dev | Star Trek (crew coordination, logs, reviews) |
| 9 | Databases: Relational & Non-Relational | Austen (social networks = relational data) |
| 10 | OS, Networks, Cloud & Web | Classic crime films (networks, heists, coordination) |
| 11 | Cybersecurity & Secure Software Dev | Classic horror (threats, defenses, monsters) |
| 12 | AI, ML & Ethics | Classic comic books (power + responsibility) |
