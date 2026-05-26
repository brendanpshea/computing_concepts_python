# COMP 1150: Computer Science Concepts — Summer 2026 Redesign

**Instructor:** Brendan Shea, PhD
**Last revised:** April 2026

This document outlines the planned redesign of COMP 1150 for summer 2026. All 12 notebooks will be rewritten; 12 case studies will be refreshed; a Flask-based final project replaces the prior capstone structure.

---

## Design Principles

1. **AI-assisted development from day one.** Students begin using an LLM as a coding partner in Notebook 1 and build explicit skills in prompt craft, verification, and critical evaluation of AI output across the semester.
2. **Critical thinking as a through-line.** Every notebook pairs with a case study that demands systematic analysis before accepting conclusions (RCTC Core Outcome).
3. **Everything builds toward the Flask app.** Databases, APIs, security, and AI features are introduced with an eye toward their role in the final project.
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
- Preview: how the Flask app will use a database

### NB 10 — OS, Networks, Cloud & the Web
**LOs:** 3
- OS concepts: processes, files, memory management (conceptual level)
- TCP/IP, HTTP, DNS
- Cloud service models: IaaS, PaaS, SaaS
- REST APIs; the `requests` library
- **First Flask "Hello World" in Colab with `pyngrok` tunneling**
- Request/response cycle; templates as preview

### NB 11 — Cybersecurity & Secure Software Development
**LOs:** 12
- CIA triad: confidentiality, integrity, availability
- Common threats: SQL injection, XSS, CSRF, brute-force, phishing
- Input validation and sanitization
- Hashing vs. encryption; salting passwords
- Secrets management (environment variables, never-commit rules)
- Each topic tied directly to what the Flask final needs

### NB 12 — AI, Machine Learning & Ethics
**LOs:** 10, 11
- Supervised vs. unsupervised learning
- Neural networks and the perceptron (conceptual + minimal code)
- LLMs: tokenization, training, inference; what they are and aren't
- Ethics in depth: algorithmic bias, privacy, labor displacement, environmental cost
- Accountability: who is responsible when AI fails?

---

## Final Project: Flask Web App

Students build a small full-stack Flask application that integrates the major threads of the course.

### Required integrations
- **Database** — SQLite or document-store, with at least two tables/collections (NB 9)
- **External API call** — any public API (NB 10)
- **AI feature** — an LLM call (summarizer, chatbot, classifier, recommender, etc.) (NB 12)
- **At least two security practices** — parameterized queries, input validation, password hashing, or secrets management (NB 11)
- **Git-tracked repo** — README, meaningful commits, and a written reflection (NB 8)

### Primary deployment target: Colab + pyngrok
Students develop and demonstrate in Colab with `pyngrok` tunneling a public URL. This keeps the toolchain consistent with the rest of the course and avoids external signups for the assessed submission.

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

The syllabus lists: Tests, Lab exercises, Assignments, Comprehensive final test (written).

Proposed structure:
- **Lab exercises** — embedded in each notebook; autograded where possible
- **Assignments** — one per notebook, building toward the Flask app (e.g., NB 9 assignment asks students to design the data model for their app)
- **Tests** — midterm after NB 6, second test after NB 10
- **Final** — comprehensive written test covering concepts + Flask project submission + brief demo

---

## Open Questions / Next Steps

1. **Notebook authoring order.** Suggest drafting NB 1, NB 8, and the Flask final-project handout first — these set the tone and the capstone target. Then fill in the rest.
2. **AI tool choice.** Pick a primary LLM for student use (Claude.ai free tier? Gemini in Colab? ChatGPT?) and standardize examples against it, with notes on the others.
3. **Case study format.** Retain the existing PDF format, or move to markdown for easier iteration?
4. **Pyngrok vs. Colab's built-in tunneling.** Confirm which is currently the most reliable path for Flask-in-Colab as of summer 2026 before committing in the handout.
