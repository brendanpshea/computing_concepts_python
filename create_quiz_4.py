import json
import os

quiz_data = {
  "title": "Chapter 4 - Control Flow and Functions",
  "shuffle_answers": True,
  "questions": [
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What happens if an `if` statement's condition evaluates to `False`?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Skips the block entirely", "correct": True },
        { "text": "Runs block one time", "correct": False },
        { "text": "Crashes the program", "correct": False },
        { "text": "Repeats the block", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "single word or term",
      "prompt": "In an `if`/`elif`/`else` sequence, how many branches can execute?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "One", "correct": True },
        { "text": "All", "correct": False },
        { "text": "None", "correct": False },
        { "text": "Two", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "When evaluating conditions joined by `and`, what happens if the first condition is `False`?",
      "answer_explanation": "This is known as short-circuiting.",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Skips evaluating the rest", "correct": True },
        { "text": "Evaluates next condition", "correct": False },
        { "text": "Throws indentation error", "correct": False },
        { "text": "Flips result to True", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "How does an `or` condition behave when evaluated?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "True if one is True", "correct": True },
        { "text": "True if both are True", "correct": False },
        { "text": "Checks second operand only", "correct": False },
        { "text": "Inverses boolean value", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What is the primary danger of writing a `while` loop?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Creating infinite loops", "correct": True },
        { "text": "Using too many variables", "correct": False },
        { "text": "Triggering syntax errors", "correct": False },
        { "text": "Returning prematurely", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "single word or term",
      "prompt": "What keyword conditionally executes exactly one of many code blocks?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "elif", "correct": True },
        { "text": "loop", "correct": False },
        { "text": "def", "correct": False },
        { "text": "return", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "Which logic limit states no program can predict if every program will eventually stop?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Halting problem", "correct": True },
        { "text": "Infinite loop paradox", "correct": False },
        { "text": "Structured program theorem", "correct": False },
        { "text": "Boolean circuit limit", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What does a `for` loop combined with `range(1, 4)` do?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Executes exactly three times", "correct": True },
        { "text": "Executes exactly four times", "correct": False },
        { "text": "Repeats indefinitely", "correct": False },
        { "text": "Starts counting at zero", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "When looping directly over a list, what does the loop variable typically represent?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Each item in turn", "correct": True },
        { "text": "Total item count", "correct": False },
        { "text": "Alphabetical order", "correct": False },
        { "text": "Fixed math value", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What is the purpose of the accumulator pattern inside a loop?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Add a running total", "correct": True },
        { "text": "Stop immediately", "correct": False },
        { "text": "Hide data locally", "correct": False },
        { "text": "Call a function", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What happens when a loop encounters the `break` keyword?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Leaves loop entirely", "correct": True },
        { "text": "Skips current pass", "correct": False },
        { "text": "Triggers an error", "correct": False },
        { "text": "Restarts from beginning", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "single word or term",
      "prompt": "If a loop running 3 times is inside one running 4 times, how many runs occur inner body?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Twelve", "correct": True },
        { "text": "Seven", "correct": False },
        { "text": "Three", "correct": False },
        { "text": "Four", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "Why was the `goto` command retired from modern programming languages?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Created tangled code", "correct": True },
        { "text": "Required more memory", "correct": False },
        { "text": "Failed math loops", "correct": False },
        { "text": "Interfered with addition", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What principle advises solving problems by breaking them into smaller sub-problems?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Top-down design", "correct": True },
        { "text": "Short-circuiting", "correct": False },
        { "text": "Iteration", "correct": False },
        { "text": "Boolean logic", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What does the `return` keyword do inside a function?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Hands one value back", "correct": True },
        { "text": "Prints a sentence", "correct": False },
        { "text": "Ends program", "correct": False },
        { "text": "Allows multiple outputs", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What happens if a Python function finishes without returning?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Automatically returns None", "correct": True },
        { "text": "Crashes with error", "correct": False },
        { "text": "Returns zero", "correct": False },
        { "text": "Locks infinite loop", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "How does defining a variable inside a function affect its scope?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Becomes local and hidden", "correct": True },
        { "text": "Overrides globals", "correct": False },
        { "text": "Modifiable everywhere", "correct": False },
        { "text": "Becomes a parameter", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What programming practice does the DRY principle promote?",
      "answer_explanation": "DRY stands for Don't Repeat Yourself.",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Write once and reuse", "correct": True },
        { "text": "Pass inputs via print", "correct": False },
        { "text": "Create identical code", "correct": False },
        { "text": "Use global variables", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What does the `help()` function output when called on a user-defined function?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "The function's docstring", "correct": True },
        { "text": "Function source code", "correct": False },
        { "text": "Current variables", "correct": False },
        { "text": "Debugging report", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "When defining parameters, what rule applies to default values?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Must follow non defaults", "correct": True },
        { "text": "Must all have defaults", "correct": False },
        { "text": "Ignored unless named", "correct": False },
        { "text": "Cannot be numeric", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What advantage does calling a function with keyword arguments offer?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Order stops mattering", "correct": True },
        { "text": "Executes faster", "correct": False },
        { "text": "Generates docstring", "correct": False },
        { "text": "Bypasses restrictions", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "Why do software developers test their code rigorously with edge cases?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Find bugs hidden normally", "correct": True },
        { "text": "Increase code speed", "correct": False },
        { "text": "Practice commands", "correct": False },
        { "text": "Bypass formatting", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "single word or term",
      "prompt": "Which control flow operation handles branching automatically?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Selection", "correct": True },
        { "text": "Sequence", "correct": False },
        { "text": "Iteration", "correct": False },
        { "text": "Accumulation", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "Which of the following operations are required parts of a safe `while` loop?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Initialise", "correct": True },
        { "text": "Test", "correct": True },
        { "text": "Progress", "correct": True },
        { "text": "Reverse", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "Which control flow structures are part of the structured program theorem?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Sequence", "correct": True },
        { "text": "Selection", "correct": True },
        { "text": "Iteration", "correct": True },
        { "text": "Accumulation", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "single word or term",
      "prompt": "Which operators are used to combine or flip boolean conditions natively in Python?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "and", "correct": True },
        { "text": "or", "correct": True },
        { "text": "not", "correct": True },
        { "text": "else", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "What are common edge cases to test for when writing a loop or function?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Empty list", "correct": True },
        { "text": "Negative number", "correct": True },
        { "text": "Boundary value", "correct": True },
        { "text": "Missing syntax", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "Which of the following statements about functions are true?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: conceptual"],
      "choices": [
        { "text": "Hides implementation details", "correct": True },
        { "text": "Takes keyword arguments", "correct": True },
        { "text": "Defines local scope", "correct": True },
        { "text": "Always returns string", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "A developer wants to skip the current loop pass, but NOT leave entirely. Which statements apply?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Use continue keyword", "correct": True },
        { "text": "Pass remainder is skipped", "correct": True },
        { "text": "Jumps to next iteration", "correct": True },
        { "text": "Use break keyword", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "How does the `if` / `elif` / `else` block sequence execute?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: notebook", "type: technical"],
      "choices": [
        { "text": "Conditions are checked from top to bottom", "correct": True },
        { "text": "The first branch evaluating to True wins", "correct": True },
        { "text": "The else branch requires an explicit condition", "correct": False },
        { "text": "Multiple branches can run in one pass", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What was the critical physical flaw in the Therac-25's X-ray mode execution?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "High energy beam fired without target", "correct": True },
        { "text": "Launched electron mode at random", "correct": False },
        { "text": "Generated too little dose", "correct": False },
        { "text": "Console destroyed output log", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "In the Therac-25 case, what clearly defines a software 'race condition'?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Outcome depends on operation timing", "correct": True },
        { "text": "Loop runs faster than CPU", "correct": False },
        { "text": "Simultaneous user login attempts", "correct": False },
        { "text": "Typing slower than required", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "Why was the 256th keypress significantly dangerous in the Yakima accident?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Counter overflowed skipping safety check", "correct": True },
        { "text": "Operator pressed proceed too often", "correct": False },
        { "text": "Hardware rotated too many times", "correct": False },
        { "text": "Memory buffer was completely full", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "According to the Systems Reply, why did older machines not kill patients despite sharing code?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Kept independent hardware safety interlocks", "correct": True },
        { "text": "Impossible to fire beam", "correct": False },
        { "text": "Slower processors prevented races", "correct": False },
        { "text": "Operators possessed superior training", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What exact message did operators see on the console during the Tyler hospital accidents?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "MALFUNCTION 54 with treatment pause", "correct": True },
        { "text": "FATAL OVERDOSE with system halt", "correct": False },
        { "text": "TARGET NOT IN SECURE PLACE", "correct": False },
        { "text": "Console powered strictly down", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What critical fallacy describes assuming software is safe because it ran previously without issue?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "The reuse fallacy", "correct": True },
        { "text": "The halting problem", "correct": False },
        { "text": "The hardware interlock", "correct": False },
        { "text": "Top down assumption", "correct": False }
      ]
    },
    {
      "question_type": "MC",
      "answer_style": "clause",
      "prompt": "What does the Accountability Objection specifically argue against the Systems Reply?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Diffuse causes retain specific decision responsibility", "correct": True },
        { "text": "Hardware interlocks caused the failure purely", "correct": False },
        { "text": "System failed naturally without intervention", "correct": False },
        { "text": "Original programmer holds total blame securely", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "Which independent decisions contributed to the entire Therac-25 system failure?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Removing independent hardware interlocks", "correct": True },
        { "text": "Lacking external safety review", "correct": True },
        { "text": "Issuing cryptic error messages", "correct": True },
        { "text": "Replacing the metal target", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "What characteristics do Therac-25 bugs share with other disasters like the 737 MAX?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Removing redundancy for cost", "correct": True },
        { "text": "Trusting optimistic risk numbers", "correct": True },
        { "text": "Positioning operators for blame", "correct": True },
        { "text": "Missing simple syntax errors", "correct": False }
      ]
    },
    {
      "question_type": "MR",
      "answer_style": "clause",
      "prompt": "Which factors specifically contributed to the 'edit race' fatal outcome?",
      "answer_explanation": "",
      "points": "",
      "tags": ["source: case-study", "type: conceptual"],
      "choices": [
        { "text": "Shared flag without locks", "correct": True },
        { "text": "Target taking eight seconds", "correct": True },
        { "text": "Operator typing edit quickly", "correct": True },
        { "text": "One byte counter overflowing", "correct": False }
      ]
    }
  ]
}

os.makedirs('perrusall_quizzes/sources', exist_ok=True)
with open('perrusall_quizzes/sources/chapter-04-controlflow-functions.quiz.json', 'w') as f:
    json.dump(quiz_data, f, indent=2)
print("Quiz rewritten successfully.")