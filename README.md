# Computing Concepts with Python

Open-access course materials for an introductory computer-science class
— twelve Jupyter notebooks, twelve short case studies, and a few small
interactive tools. Used in **COMP 1150** at Rochester Community and
Technical College and freely adaptable elsewhere.

**Live site:** <https://brendanpshea.github.io/computing_concepts_python/>

**Author:** Brendan Shea, PhD ([brendan.shea@rctc.edu](mailto:brendan.shea@rctc.edu))

**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — adapt and remix freely with credit.

---

## For students

Start at the [course page](https://brendanpshea.github.io/computing_concepts_python/summer_2026/).
Each week pairs a **notebook** with a short **case study**:

- The notebook is a Jupyter notebook. Open it in Google Colab, run the
  cells, and try the exercises.
- The case study is a 20–30 minute read about the people, history, and
  arguments behind the technical material. The discussion questions
  have no answer key — they are for arguing about with other people.

## For instructors

Everything is CC BY 4.0. Adapt, remix, fork. The
[course outline](summer_2026/course_outline.md) shows the twelve-week
sequence, the design rationale, and the through-lines that connect the
case studies to the notebooks.

Case studies are written in [Quarto](https://quarto.org/) so they can
be re-rendered to HTML, DOCX, or PDF, and re-skinned for a different
course. See [`summer_2026/case_study_style_guide.md`](summer_2026/case_study_style_guide.md)
for the conventions; [`summer_2026/cases/case_study_template.qmd`](summer_2026/cases/case_study_template.qmd)
is a fill-in-the-blanks template.

To build the site locally:

```bash
# install Quarto: https://quarto.org/docs/get-started/
quarto render            # builds the whole site into ./docs/
quarto preview           # local server with live reload
```

---

## Repo layout

```
.
├── index.qmd                       site landing page
├── summer_2026/                    CURRENT COURSE
│   ├── index.qmd                   course landing
│   ├── notebooks/                  twelve Jupyter notebooks
│   ├── cases/                      twelve case studies (Quarto)
│   ├── course_outline.md           sequence, rationale, design notes
│   ├── notebook_template.md        notebook authoring guide
│   └── case_study_style_guide.md   case-study authoring guide
├── archive/                        previous versions (2024)
├── tools/                          small interactive tools
│   ├── python_code_quiz/           PyQuiz — IPython-widget practice
│   └── object_quest/               RPG-style quiz game
├── docs/                           rendered HTML (served by GitHub Pages)
├── _quarto.yml                     site configuration
└── LICENSE
```

## Interactive tools

- **[PyQuiz](tools/python_code_quiz/readme.md)** — a Python coding-practice
  tool built on IPython widgets, runs in any Jupyter environment.
- **[ObjectQuest](tools/object_quest/)** — a small RPG-style quiz game
  for object-oriented practice.

## Contributing

Issues and pull requests welcome. For substantive changes to the
case-study content or pedagogy, please open an issue first.
