# Perusall Quiz Workflow

This folder now supports a two-step workflow:

1. Author or edit rich source files in `sources/*.quiz.json`.
2. Generate Perusall-ready CSV files from those sources.

The generated CSVs stay flat and importable. The source files hold the extra metadata that is hard to manage in CSV alone, especially `answer_style` and free-form `tags`.

## Source Format

Each source file is a `.quiz.json` document with this shape:

```json
{
  "title": "Chapter 1 - Notebook and Case Study",
  "shuffle_answers": true,
  "questions": [
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What does a Turing machine mathematically model of?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "topic: turing-machine"],
      "choices": [
        { "text": "The physical construction of CPUs", "correct": false },
        { "text": "The logical limits of computation", "correct": true },
        { "text": "The syntax of early compilers", "correct": false },
        { "text": "The storage capacity of memory", "correct": false }
      ]
    }
  ]
}
```

## `answer_style` Values

Use these exact values:

- `single word or term`: one-word answers, short terms, or very short noun phrases.
- `clause`: short clauses or compact phrases that usually run about 3 to 7 words.
- `complete sentence`: full-sentence options. Use sparingly so the quiz-wide average still stays below 5 words.

The generator and validator do not force a rigid length for every individual option, but they do report style mismatches and still enforce the quiz-wide average answer-length target.

## Commands

Convert existing flat CSVs into richer source files:

```powershell
python .\perrusall_quizzes\convert_perusall_csv_to_source.py .\perrusall_quizzes --output-dir .\perrusall_quizzes\sources
```

Generate CSVs from source files. Answer choices are shuffled by default with a reproducible seed:

```powershell
python .\perrusall_quizzes\generate_perusall_quiz.py .\perrusall_quizzes\sources --output-dir .\perrusall_quizzes
```

Validate the generated CSVs:

```powershell
python .\perrusall_quizzes\validate_perusall_csv.py .\perrusall_quizzes
```

If you only need to reshuffle an already-written CSV, the legacy flat-file script still exists:

```powershell
python .\perrusall_quizzes\shuffle_perusall_answers.py .\perrusall_quizzes
```

## Recommended Practice

- Edit the `.quiz.json` files, not the generated CSVs, unless you are making a quick emergency fix.
- When including code in prompts or answers, wrap it in backticks (`like this`). The validator ignores text in backticks during reading-level checks. Furthermore, commas and quotes in code can break CSV flat files, making `.quiz.json` editing safer.
- Keep `tags` structured so you can track quiz balance. Use tags like `"source: notebook"`, `"source: case-study"`, `"type: conceptual"`, and `"type: technical"` to quickly eyeball question ratios.
- Ask about the underlying concept, algorithm, case fact, or doctrine, not the course packaging. Avoid prompts framed around `this notebook`, `this cell`, `this case study`, or `this lecture`.
- When a prompt asks for a named term, preserving the canonical label verbatim is fine. Do not replace terms like `polymorphism` or `encapsulation` with generic descriptions if the question tests vocabulary recognition.
- Avoid prompt wording that cues the answer by repeating its stem.
- When a question is about events, facts, operations, or code execution output, write the answer choices as clauses or complete sentences. Use periods on complete-sentence choices.
- Do not use placeholder answers like `Line 5` or `Cell 2`. Put the actual code chunk or algorithmic logical step in the answer choices.
- Use `complete sentence` only where the question actually benefits from full-sentence distractors.
- Run generation and validation together after every batch of edits.