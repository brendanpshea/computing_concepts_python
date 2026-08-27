# COMP 1150: Computer Science Concepts — Second Edition Design Notes

**Instructor:** Brendan Shea, PhD
**Written:** April 2026, for the summer 2026 redesign · **Revised:** August 2026 for fall 2026

This document records the design of the second edition of COMP 1150 — the rationale, the twelve-week sequence, and the through-lines connecting the case studies to the notebooks. It was written as a plan for the summer 2026 rebuild and is kept as the reference for anyone adopting or adapting the course.

> **The syllabus is authoritative for how the course is actually run.** Where this document and the current syllabus disagree about assessment, dates, or requirements, follow [`syllabi/syllabus_fa26.md`](../syllabi/syllabus_fa26.md). The "Assessment Alignment" section below has been updated to match it.

---

## Design Principles

1. **AI-assisted development from day one.** Students begin using an LLM as a coding partner in Notebook 1 and build explicit skills in prompt craft, verification, and critical evaluation of AI output across the semester.
2. **Critical thinking as a through-line.** Every notebook pairs with a case study that demands systematic analysis before accepting conclusions (RCTC Core Outcome).
3. **Everything builds toward something shippable.** Databases, APIs, security, and AI features are introduced with an eye toward the optional final project — a Python program of the student's own design, for which a small Flask app is the most ambitious path.
4. **Philosophical, not mathematical, treatment of computability.** The limits of computation are presented as conceptual boundaries of what machines can do, not as formal proofs.

---

## Mapping to Student Learning Outcomes

| LO | Outcome | Primary notebook(s) |
|----|---------|---------------------|
| 1 | Machine architecture, data representation, processor-memory interaction | NB 2 |
| 2 | Data storage, number systems, binary representation | NB 2 |
| 3 | OS, networking, cloud computing, the web | NB 10 |
| 4 | Algorithmic concepts for problem solving | NB 3, 4, 7 |
| 5 | Pseudocode and flowcharts | NB 3 |
| 6 | Python implementation of algorithmic solutions | NB 3, 4, 5, 6 |
| 7 | SDLC, version control, AI-assisted development | NB 1 (intro), NB 8 (depth) |
| 8 | Modular design, abstraction, ADTs | NB 5, 6 |
| 9 | Relational vs. non-relational databases | NB 9 |
| 10 | AI and machine learning core concepts | NB 12 |
| 11 | Ethics: bias, privacy, societal impact | NB 1, 12 + every case study |
| 12 | Cybersecurity and secure software development | NB 11 |
| 13 | Computability and limits of computation | NB 7 |

---

## 12-Notebook Sequence

### NB 1 — What Is Computing? A Story of Four Algorithms
**LOs:** 4, 7, 11
- CS as a field: history, subfields, what computer scientists actually do (study algorithms at many different levels-- part math, stats, engineering, philosophy, etc.)
- Colab environment: cells, runtime, saving to Drive/GitHub
- Using Gemini in Colab (chat, in-line, agent)
- FOUR ALGORITHMS (need to talk about history/context/importance, simple algorithm in pseudode and basic python)
-  Ada Lovelace's Algorithm
- Processing Census Data 
- Breaking Enigma (simplified)
- ELIZA
- Exercises throughout have students use AI to alter the simple algorithms we've laid out 

### NB 2 — Machine Architecture & Data Representation
**LOs:** 1, 2
- Von Neumann architecture: CPU, memory, storage, I/O
- Binary, hexadecimal, two's complement
- Encoding text (ASCII, Unicode), images, sound
- Why representation matters for correctness and security
- Python bit operations and conversion functions
- Throughout, some history of CS from 1945 to the present (building on lecture 1)

### NB 3 — Python Basics via Pseudocode & Flowcharts
**LOs:** 5, 6
- Variables, types, operators, expressions
- Pseudocode conventions and flowchart notation
- Workflow: problem → pseudocode → flowchart → Python
- AI-assisted translation exercises ("here's my pseudocode, generate Python, I verify")
- Reading code the AI produces and catching errors

### NB 4 — Control Flow & Functions
**LOs:** 4, 6, 8
- Conditionals, loops (for/while), nested logic, break/continue
- Decomposing problems into subproblems
- Functions, parameters, return values, scope
- Testing your logic with edge cases

### NB 5 — Collections & Abstract Data Types
**LOs:** 6, 8
- Lists, tuples, dicts, sets — when to use each
- List/dict comprehensions
- Abstract data types as a concept: interface vs. implementation
- Choosing the right data structure for a task

### NB 6 — Modules & Object-Oriented Design
**LOs:** 6, 8
- Modules and imports
- Classes, objects, attributes, methods
- Inheritance and encapsulation at an introductory level
- Abstraction as the OOP payoff

### NB 7 — Algorithms, Complexity & the Limits of Computation
**LOs:** 4, 13
- Linear and binary search; bubble, insertion, and merge sort. 
- Big O notation (conceptual, not heavy math)
- **Philosophical treatment of computability:**
  - Turing machines as a thought experiment
  - The halting problem: why some things can't be computed
  - P vs. NP as a cultural idea: "easy to check, hard to solve"
  - What does it mean for a problem to be "undecidable"?
- Connection to modern AI: what LLMs can and cannot do in principle

### NB 8 — Software Engineering: SDLC, Git & AI-Assisted Development
**LOs:** 7
- Software development lifecycle: requirements → design → implementation → testing → maintenance
- Waterfall vs. Agile
- Git/GitHub from Colab: clone, commit, push, branch, pull request
- AI-assisted workflows: spec → code → test → review loop
- Code review as a skill; reading PRs; writing clear commit messages
- Testing basics: unit tests, assertions

### NB 9 — Databases: Relational & Non-Relational
**LOs:** 9
- Relational model and SQL fundamentals (CREATE, INSERT, SELECT, JOIN, GROUP BY)
- SQLite in Colab
- Non-relational models: document stores (JSON using SQLite)
- When to use which: tradeoffs in flexibility, consistency, scale
- Preview: how a small web app would use a database

### NB 10 — OS, Networks, Cloud & the Web
**LOs:** 3
- OS concepts: processes, files, memory management (conceptual level)
- TCP/IP, HTTP, DNS
- Cloud service models: IaaS, PaaS, SaaS
- REST APIs; the `requests` library
- **First Flask "Hello World" in Colab, served through Colab's built-in port tunnelling**
- Request/response cycle; templates as preview

### NB 11 — Cybersecurity & Secure Software Development
**LOs:** 12
- CIA triad: confidentiality, integrity, availability
- Common threats: SQL injection, XSS, CSRF, brute-force, phishing
- Input validation and sanitization
- Hashing vs. encryption; salting passwords
- Secrets management (environment variables, never-commit rules)
- Each topic tied to what a student would need to build a small app of their own

### NB 12 — AI, Machine Learning & AI
**LOs:** 10, 11
- Supervised vs. unsupervised learning
- Neural networks and the perceptron (conceptual + minimal code)
- LLMs: tokenization, training, inference; what they are and aren't
- Ethics in depth: algorithmic bias, privacy, labor displacement, environmental cost
- Accountability: who is responsible when AI fails?

---

## Final Project

**As taught in fall 2026 the project is optional and worth extra credit**, and the requirements are deliberately light: any Python program of the student's own design, in a Colab notebook or as a standalone script, with a README, a short AI-use reflection, a GitHub repo, and a two-to-three minute video demo. [`FINAL_PROJECT_SPEC.md`](../FINAL_PROJECT_SPEC.md) is the authoritative statement of what is required; this section records the more ambitious version the course was originally designed around, for anyone who wants to assign it.

### The ambitious version: a small full-stack Flask app
A student who wants to use everything the course covers can build a web application integrating the major threads:

- **Database** — SQLite or document-store, with at least two tables/collections (NB 9)
- **External API call** — any public API (NB 10)
- **AI feature** — an LLM call (summarizer, chatbot, classifier, recommender, etc.) (NB 12)
- **At least two security practices** — parameterized queries, input validation, password hashing, or secrets management (NB 11)
- **Git-tracked repo** — README, meaningful commits, and a written reflection (NB 8)

None of these are required under the fall 2026 spec. They are a menu, and a student who builds a text adventure with a save file has met the actual requirement.

### Development and demo target: Colab
Students develop and demonstrate in Colab, serving the app through Colab's built-in port tunnelling (`serve_kernel_port_as_iframe` / `serve_kernel_port_as_window`, as in NB 10). This keeps the toolchain consistent with the rest of the course and avoids external signups. `pyngrok` remains an option for a public URL reachable off Colab, at the cost of a free ngrok account and token.

### Alternative hosting paths (documented in final-project handout)
Provided for students who want to take their project further:
- **Render** — free web service tier, connects to GitHub repo, auto-deploys on push
- **Fly.io** — free tier, `flyctl` deploy from local/Colab
- **PythonAnywhere** — free tier, simplest Flask-specific hosting
- **Replit** — deploy button, good for quick prototypes
- **Hugging Face Spaces (Gradio alternative)** — for AI-heavy projects

Each option will include: setup walkthrough, secrets handling, limits of the free tier, and a one-line "choose this if..." recommendation.

### Suggested project themes
- Personal book/movie tracker with AI recommendations
- Recipe generator (pantry → recipe via LLM)
- Study-flashcard app with LLM-generated questions from pasted notes
- News summarizer pulling from an API
- Budget tracker with AI-generated spending insights
- Journal with AI-assisted reflection prompts

---

## 12 Case Studies

Each case study pairs with a notebook and is designed around the RCTC Critical Thinking outcome: students must evaluate evidence and competing claims before drawing conclusions.

| # | Title | Pairs with | Status |
|---|-------|-----------|--------|
| 1 | The Lovelace–Turing Debate: Can Machines Think — and Who Gets to Build Them? | NB 1 | New. Focus = the "can machines think / what follows" argument + who is counted into CS (women & minorities). Avoids hagiography by staying on the debate. |
| 2 | Chip Wars & Moore's Law — TSMC, export controls, silicon geopolitics | NB 2 | New. Tighten the data-representation/architecture link so NB 2 concepts are load-bearing. |
| 3 | Grace Hopper, Compilers & the Abstraction Bargain | NB 3 | New. Abstraction that hides danger — runs from the first compilers through to LLM code generation. |
| 4 | The Therac-25 Disaster — when control flow kills | NB 4 | New. **Template pilot.** |
| 5 | How We Represent People: ADTs and the Ethics of Data Modeling | NB 5 | Replaces old "Number Zero." ADT/collection design as a moral choice (name, gender, race, `null`); incorporates AI training-data categories. |
| 6 | Was OOP a Mistake? Alan Kay, Smalltalk & the Backlash | NB 6 | New. Reframed from "the OOP vision" into the genuine two-sided OOP debate. |
| 7 | The Halting Problem & the Limits of Machines | NB 7 | New. |
| 8 | Open Source & the Code an AI Learned From — Linux, Git & Copilot | NB 8 | New, narrowed. Open-source labor/sustainability + the Copilot/training-data copyright fight. Waterfall/Agile stays notebook-only content, not a case. |
| 9 | From SQL to NoSQL — Why Google Built Bigtable | NB 9 | New. |
| 10 | Three Companies Own the Internet — ARPANET to the Cloud Oligopoly | NB 10 | New. Sharpened from a history tour to the centralization/fragility debate. |
| 11 | The Equifax Breach | NB 11 | Keep existing. |
| 12 | COMPAS, Facial Recognition & AI Accountability | NB 12 | Replaces old "AI Ethics." |

**Dropped from prior set:** Functionalism (philosophy detour not aligned to new LOs), War and Technology (coverage absorbed into Chip Wars + the Lovelace–Turing case). **Waterfall/Agile** is no longer a standalone case — it lives as NB 8 notebook content; the NB 8 case now spends its discussion budget on open source + AI-trained-on-open-source instead.

**AI as a through-line in the cases:** beyond NB 12, the AI/LLM debate is deliberately threaded through Cases 1 (can machines think), 3 (abstraction hiding danger → LLM codegen), 5 (training-data categories), and 8 (Copilot & open-source code). This mirrors the notebooks' "AI-assisted development from day one" spine so the cases interrogate the tool the course itself uses.

---

## Assessment Alignment

As taught in **fall 2026** (see the syllabus for dates and exact weights):

| Component | Weight | Notes |
|---|---:|---|
| Four proctored exams | 60% | 15% each, 75 minutes, covering the three chapters since the last exam. Mostly objective questions plus a few short coding questions, each closing with one essay on a case study. |
| Lectures and case studies on Perusall | 25% | Annotation quality, active reading time, and engagement with classmates. No Perusall quizzes this term. |
| *Loop of the Recursive Dragon* | 10% | Self-paced Python practice delivered in D2L as a SCORM module; unlimited retries. |
| Week 1 pre-test | 5% | Proctored, unlimited attempts. Doubles as the Respondus setup check for the online section. |
| Optional final programming project | extra credit | Any Python project; see `FINAL_PROJECT_SPEC.md`. Not required, and cannot lower a grade. |

Exams fall after chapters 3, 6, 9, and 12. Two notes for anyone adapting this:

- **The notebooks carry the practice, not the grade.** The `✏️ Your Turn` cells, the PyQuiz banks, and the capstones are formative — nothing in a notebook is collected. The graded practice lives in *Loop of the Recursive Dragon*.
- **Every exam ends on a case study essay.** That is what makes the case studies load-bearing rather than optional enrichment, and it is why each one closes with arguments laid out in premise-conclusion form.

---

## Open Questions — Resolved

The questions this document opened in April 2026 have since been settled by the build:

1. **Notebook authoring order.** ~~Draft NB 1, NB 8, and the final-project handout first.~~ All twelve notebooks and twelve case studies are written and published.
2. **AI tool choice.** ~~Pick a primary LLM and standardize examples against it.~~ Resolved as *no single tool*: the notebooks name Gemini (built into Colab), Claude, and ChatGPT interchangeably, and the exercises are written to work with any of them. The transferable skill is verification, not one vendor's interface.
3. **Case study format.** ~~PDF or markdown?~~ Resolved as Quarto `.qmd`, rendering to HTML for the site and DOCX for print. The 2024 PDFs are preserved in `archive/`.
4. **Pyngrok vs. Colab's built-in tunneling.** Resolved in favour of Colab's built-in tunnelling — Notebook 10 uses `serve_kernel_port_as_iframe` and `serve_kernel_port_as_window`, which need no account or token. `pyngrok` is mentioned only as an optional side quest for students who want a URL reachable off Colab.

## The Career Strand

Every notebook carries a three-cell **💼 block** before its Key Terms: a real
job the chapter's material belongs to, its figures, and a Think About It.
Eight are occupations, four are processes (the shape of the field, reading a
job posting, the technical interview, the first ninety days) — because there
are not twelve distinct junior roles to hand out.

Three decisions worth recording:

- **Figures are generated, never typed.** `tools/career_data.py` is the single
  source for every number, each with a source URL, an as-of date and a
  confidence flag; `--check` reports drift and refuses to pass on an
  unestablished figure. Twelve notebooks of hand-typed salaries would be
  twelve archaeology jobs each August.
- **Projections always print their base year.** A BLS projection is a model
  run from a base year, and the 2024-2034 round predates the entry-level
  contraction the New York Fed's current numbers show. Notebook 1 makes that
  disagreement the lesson rather than hiding it — which is also the cleanest
  Critical Thinking artifact in the course.
- **The strand tests the course's own argument.** The Hopper case study's
  Labor Reply claims every abstraction displaces a category of worker, junior
  developers writing boilerplate included. The career blocks are the empirical
  running commentary on that claim, and Notebook 12 closes the loop.

## Still Open

- **Lecture videos.** The placeholder links have been removed from the notebooks; add real links when the recordings exist.
- **Career figures are second-hand.** Every row in `tools/career_data.py` was
  assembled from search results quoting the BLS pages rather than read off
  bls.gov directly, and one (database administrator median) is not yet
  established at all. Confirming a row is one click and one word; `--check`
  lists what remains.
- **PyQuiz coverage.** Banks exist for notebooks 3–5 only. Decide whether to extend the set to 6–12 or leave the later chapters to *Loop of the Recursive Dragon*.
