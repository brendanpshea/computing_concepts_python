# Case Study Template & Style Guide — Summer 2026

Authoring guide for the 12 COMP 1150 case studies. Companion to
`notebook_template.md`. Each case study pairs with exactly one notebook
(see the table in `course_outline.md`) and is written in Quarto
(`.qmd`) against the shared `refs.bib`. The format is modeled on the
attached bioethics case ("Dax Cowart") — narrative, then a connected
argument dialogue, then discussion.

---

## Targets at a Glance

| Spec | Target |
|------|--------|
| Core prose | ~3,000 words (narrative + argument dialogue) |
| Full piece | ~5,000 words with context boxes, figure caption, questions, refs |
| Reading level | 11th–14th grade (a step above the notebooks; this is the reflective half of the course) |
| Source format | Quarto `.qmd` → HTML + PDF |
| Bibliography | shared `refs.bib`, BibTeX, `@citekey` |
| Argument blocks | 3–5, **connected** (each answers the prior) |
| Discussion questions | 5, no single right answer |
| Figures | 0–1, graphviz `{dot}`, only if a process/decision needs it |
| Images | avoid; if used, generated or public-domain with credit |

---

## The Two Jobs (every case must do both)

1. **Apply the notebook's concepts.** The CS content must be
   *load-bearing* — the case turns on a race condition, a hash vs.
   encryption choice, an undecidable problem, a schema decision. A
   reader should leave understanding the concept *better*, not just
   having read history around it. Teach the concept in a
   `.context-box` exactly where the story needs it.
2. **Open a real debate.** History, ethics, or current practice in
   software engineering / security / CS theory. The point is
   discussion, not recall. There is no answer key. This is where the
   RCTC critical-thinking outcome is assessed.

If a draft only does (1) it's a notebook; if it only does (2) it's a
think-piece. It must do both, fused.

---

## Voice & Style

- **Narrative first, judgment later.** "The Case" tells the story
  straight — real named people, recognizable stakes, present tension,
  no editorializing. Earn the reader's investment before any argument.
- **Steelman everyone.** Every position in the dialogue gets its
  strongest form, in its proponents' own words where possible
  (quote + `@citekey`). The engineers under deadline, the company, the
  court — not just the sympathetic side.
- **Concrete and specific.** Dates, places, names, the actual standard
  that did or didn't exist yet. Specificity is what makes the
  historical/ethical judgment fair.
- **End on a sharper question, not a verdict.** The last move is the
  current-practice turn: where does this rest *today*, and why is it
  still unresolved?
- **Plain words for hard ideas.** Define every technical term on first
  use; mark it `[term]{.key-term}`.

---

## Structure (mirrors `case_study_template.qmd`)

1. **YAML front matter** — title, human subtitle, author *Brendan
   Shea, PhD*, `date: last-modified`, `bibliography: refs.bib`.
2. **`::: {.case-at-a-glance}`** — Who / What / Where–When / Why it
   matters / Pairs with + Concepts applied. Name the colliding forces
   as `.key-term` spans.
3. **`## The Case`** — ~1,200–1,500 words of narrative. `.context-box`
   callouts teach the paired concept where the story needs it. End on
   the unresolved human question; state that the outcome is not the
   point.
4. **`## The Argument [X] Started`** — ~1,500–1,800 words. 3–5
   *connected* `.argument` blocks (numbered premises → conclusion),
   with connective prose naming which premise each move attacks.
   Sequence: opening argument → strongest reply → counter → optional
   reframe → the empirical / current-practice turn.
5. **`## Discussion Questions`** — exactly 5 (see rule below).
6. **`## Further Reading`** — 3–5 annotated entries with `@citekey`.
7. **`## References`** — `::: {#refs}` block.

---

## The Argument Dialogue (the heart of it)

- Each `.argument` is a named, numbered reconstruction:
  premises then `Therefore,` conclusion.
- Blocks must **connect**: block N+1 attacks a specific premise of
  block N. Say which premise, in prose, between them.
- At least one block should be the **empirical / current-practice
  turn** — what recent incidents or industry behavior show, where the
  tidy lesson breaks. This keeps the debate live, not historical.
- Use the same theory vocabulary the course uses elsewhere
  (trade-offs, accountability, abstraction, undecidability, bias) so
  cases reinforce notebooks.

---

## Discussion Question Rules

- 5 questions, none with a single correct answer.
- ≥1 makes students **reconstruct two arguments and name the shared
  disputed premise**.
- ≥1 puts the student **inside the scenario as a decision-maker**.
- ≥1 connects to a **paired-notebook concept** they can run code on.
- ≥1 applies the case's framework to a **second contrasting case**.

---

## Quarto / Mechanics

- One shared `refs.bib`; cite keys `firstauthorYEAR`, grouped by case
  with comment banners. Reuse keys across cases.
- Custom callout classes (`.case-at-a-glance`, `.context-box`,
  `.argument`) and `.key-term` need styling. Add a
  `_case-styles.scss` and reference it from a project `_quarto.yml`
  before final render; drafts render fine as plain divs.
- Figures: graphviz `{dot}` only, with `//| label:` and a `//|
  fig-cap:` that explains how to read it. Color convention:
  `#dde8f0` start, `#f3e9d8` pivotal decision, `#e3efe1` endpoint.
- Attribution is **Brendan Shea, PhD**. Never Rochester Community and
  Technical College — title, body, or footer.

---

## Checklist Before Publishing a Case Study

- [ ] Pairs with exactly one notebook; concepts applied are named in the at-a-glance box
- [ ] CS concept is load-bearing, taught in a `.context-box` where the story needs it
- [ ] Narrative earns investment before any argument; no early editorializing
- [ ] 3–5 `.argument` blocks, **connected**, every side steelmanned
- [ ] Includes a current-practice / empirical turn; ends on a sharper question
- [ ] 5 discussion questions meeting all four coverage rules; none with one right answer
- [ ] Every `[term]{.key-term}` defined on first use
- [ ] Every `@citekey` resolves in `refs.bib`; Further Reading has 3–5 entries
- [ ] Figure (if any) labeled with a how-to-read caption
- [ ] All HTML authoring comments deleted
- [ ] ~5,000 words; attribution to Brendan Shea, PhD only
- [ ] Renders to HTML and PDF without errors
