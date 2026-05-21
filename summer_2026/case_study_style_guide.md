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
| Reading level | **Flesch-Kincaid grade < 9.0.** Accessible to community-college readers, including the many reading in their second language. |
| Source format | Quarto `.qmd` → HTML + PDF |
| Bibliography | shared `refs.bib`, BibTeX, `@citekey` |
| Argument blocks | 2–4, **connected** (each answers the prior); not all need formal premise/conclusion form |
| Code snippets | 0–3 short Python blocks (5–25 lines), runnable, used to *let students see the concept work* — not required, but welcome when the CS rewards it |
| Discussion questions | 5, no single right answer; mix of technical and ethical |
| Figures | 0–1, graphviz `{dot}`, only if a process/decision needs it |
| Images | avoid; if used, generated or public-domain with credit |

---

## The Three Jobs (every case must do all three)

1. **Tell the story.** Real named people, recognizable stakes,
   present tension. Earn the reader before any analysis. The history
   is the hook; do not skip it for the moral.
2. **Reinforce the CS.** The case must make the reader *understand
   and apply* the core technical concept(s) it turns on — race
   conditions, hash vs. encryption, schema choice, undecidability,
   Big-O, whatever the case is built around. A `.context-box` teaches
   the concept where the story needs it; a short Python snippet (5–25
   lines, runnable) is welcome wherever the reader benefits from
   *seeing the concept run*. The reader should leave more fluent in
   the technique, not just informed about an incident.

   **Reinforces ideas the reader is encountering elsewhere in the
   course — but never name where.** No "as we saw in the notebook,"
   no "NB 4," no "in lecture." The case should read as a standalone
   piece a student could hand to a friend.
3. **Open an ethics / governance debate.** Every case carries one
   real argument with no single correct answer — about
   responsibility, history, current practice in software engineering,
   security, or CS theory. This is where the critical-thinking
   outcome is assessed. The ethics is *one* component, not the whole
   piece; balance it with (2).

If a draft only does (2) it's a notebook; if it only does (3) it's a
think-piece. The case must do all three, fused.

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
- **Short sentences.** Aim ~15 words. Split anything over 25. The
  hardest sentences for a second-language reader are the ones with a
  semicolon, two commas, and an em-dash all carrying separate ideas
  — break those up.
- **Use lists.** When laying out a process, a sequence of steps, or
  three-or-more named items, prefer a numbered or bulleted list over
  a sentence with semicolons. Lists scan; comma-stacked sentences do
  not. The `## How It Worked` section especially benefits.

---

## Structure (mirrors `case_study_template.qmd`)

1. **YAML front matter** — title, human subtitle, author *Brendan
   Shea, PhD*, `date: last-modified`, `bibliography: refs.bib`.
2. **`::: {.case-at-a-glance}`** — Who / What / Where–When / Why it
   matters / **Concepts at play**. Name the colliding forces as
   `.key-term` spans. *Do not* reference notebooks, lectures, or the
   course structure here or anywhere else in the case body.
3. **`## The Case`** — ~1,000–1,300 words of narrative.
   `.context-box` callouts teach the concept where the story needs
   it. End on the unresolved question; state that the outcome is not
   the point.
4. **`## How It Worked`** *(or a case-fitting variant: "The Race and
   the Counter," "What the Code Was Doing," etc.)* — ~500–800 words.
   The CS-at-play section. Walk through the mechanism in enough
   detail that the reader can apply the concept later. Include 0–3
   short Python snippets where the reader benefits from *running* the
   idea — a tiny demo of the bug, the algorithm, the data structure,
   the overflow. Prose-only is acceptable when code would be
   contrived.
5. **`## The Argument [X] Started`** *(or "What's Still Argued," "The
   Open Question," etc.)* — ~1,000–1,500 words. 2–4 *connected*
   positions in tension, with connective prose naming what each move
   challenges. Use `.argument` blocks (numbered premises →
   conclusion) for the central move(s); demote secondary positions to
   labeled prose so the section does not read as a philosophy paper.
   Close with the current-practice / empirical turn and a sharper
   question.
6. **`## Discussion Questions`** — exactly 5 (see rule below).
7. **`## Further Reading`** — 3–5 annotated entries with `@citekey`.
8. **`## References`** — `::: {#refs}` block.

---

## The Argument Dialogue (the heart of it)

- Use `.argument` blocks (named, numbered premises → `Therefore,`
  conclusion) for the central tension. Two formal blocks is usually
  enough; a third is fine when the move genuinely earns it.
- Secondary positions belong in prose paragraphs with a short bold
  label ("**The accountability objection.**"). Do not stack four or
  five formal blocks — that is the philosophy-paper shape this
  template is deliberately *not*.
- Whatever shape you use, the section must still **connect**: each
  move says what it challenges in the prior move.
- Close with the **current-practice / empirical turn** — what recent
  incidents or industry behavior show, where the tidy lesson breaks.
  This keeps the debate live, not historical.
- Reach for the technical vocabulary the rest of the course uses
  (trade-offs, accountability, abstraction, undecidability, bias) so
  the case reinforces what the student is learning — without naming
  where they learned it.

---

## Discussion Question Rules

- **Plain language.** Each question is 1–3 short sentences. One main
  idea per sentence. Common words. No nested clauses, no parentheticals
  inside parentheticals, no "drawing on X and Y, do Z" stacking. Many
  students read in their second language; if a sentence has more than
  ~20 words, split it.
- 5 questions, none with a single correct answer. Mix technical and
  ethical — at least 2 of each across the set.
- ≥1 asks students to **work the CS** — modify the snippet, predict
  output, design a small change, or apply the concept to a fresh
  scenario.
- ≥1 makes students **reconstruct two positions and name what they
  actually disagree about**.
- ≥1 puts the student **inside the scenario as a decision-maker**.
- ≥1 applies the case's framework or technique to a **second
  contrasting case**.

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

- [ ] **No mention of notebooks, lectures, or the course** anywhere in the case body (the pairing is authoring metadata only)
- [ ] Concepts at play are named in the at-a-glance box
- [ ] CS concept is load-bearing — taught in a `.context-box` and/or worked through in a "How It Worked" section
- [ ] Python snippets (if any) are short, runnable, and let the reader *see the concept work*
- [ ] Narrative earns investment before any analysis; no early editorializing
- [ ] 2–4 connected positions in the argument section, every side steelmanned; no more than 2–3 formal `.argument` blocks
- [ ] Includes a current-practice / empirical turn; ends on a sharper question
- [ ] 5 discussion questions meeting the coverage rules; mix of technical and ethical; none with one right answer
- [ ] Every `[term]{.key-term}` defined on first use
- [ ] Every `@citekey` resolves in `refs.bib`; Further Reading has 3–5 entries
- [ ] Figure (if any) labeled with a how-to-read caption
- [ ] All HTML authoring comments deleted
- [ ] ~3,000 core / ~5,000 all-in words; attribution to Brendan Shea, PhD only
- [ ] **Flesch-Kincaid reading grade < 9.0**; no prose sentence over ~30 words without a real reason
- [ ] Lists used for processes and 3+-item enumerations instead of comma-stacked sentences
- [ ] Renders to HTML and DOCX without errors
