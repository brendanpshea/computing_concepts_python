import json
import os

quiz = {
  "title": "Chapter 1 - Hardware & Lovelace",
  "shuffle_answers": True,
  "questions": []
}

qa_data = [
    # NOTEBOOK: CONCEPTUAL
    ("MC", "clause", "What does computer science study?", ["source: notebook", "type: conceptual"],
     "Algorithms, data, and problem-solving", "Only how physical computer hardware is built", "How to use apps and spreadsheets", "The mechanics of repairing laptops", 1),
    ("MC", "single word or term", "Which analogy best describes the relationship between computer science and computers?", ["source: notebook", "type: conceptual"],
     "Astronomy to telescopes", "Biology to microscopes", "Chemistry to beakers", "Physics to particles", 1),
    ("MC", "clause", "What is Google Colab?", ["source: notebook", "type: conceptual"],
     "A browser-based Python environment", "A physical piece of server hardware", "A language older than Python", "A social media platform for coders", 1),
    ("MC", "clause", "What does a built-in function like `print()` do?", ["source: notebook", "type: conceptual"],
     "It performs a predefined action", "It crashes the computer if misused", "It invents a new operation", "It creates physical hardware", 1),
    ("MC", "single word or term", "Which built-in AI assistant does Colab provide?", ["source: notebook", "type: conceptual"],
     "Gemini", "Siri", "Alexa", "Cortana", 1),
    ("MC", "clause", "Why did nineteenth-century science need algorithms?", ["source: notebook", "type: conceptual"],
     "To compute long navigation tables without errors", "To browse the early internet", "To design automated steam engines", "To build early video games", 1),
    ("MC", "clause", "What was Charles Babbage's Analytical Engine intended to be?", ["source: notebook", "type: conceptual"],
     "A general-purpose mechanical computer", "The first electric supercomputer", "A calculator using vacuum tubes", "A silicon-based logic board", 1),
    ("MC", "clause", "What is the equivalent of the CPU in the Analytical Engine?", ["source: notebook", "type: conceptual"],
     "The Mill", "The Store", "The Variable Cards", "The Output Printer", 1),
    ("MC", "clause", "What is the equivalent of memory in the Analytical Engine?", ["source: notebook", "type: conceptual"],
     "The Store", "The Mill", "The Stack", "The CPU", 1),
    ("MC", "clause", "How do factorial values grow as the input sequence increases?", ["source: notebook", "type: conceptual"],
     "Explosively and non-linearly", "At a steady linear pace", "They decrease over time", "They remain exactly the same", 1),
        
    # NOTEBOOK: TECHNICAL
    ("MC", "single word or term", "What symbol is used to pass data to a function?", ["source: notebook", "type: technical"],
     "Parentheses `()`", "Brackets `[]`", "Braces `{}`", "Quotes `\"\"`", 1),
    ("MC", "clause", "In `def compute_factorials(n):`, what does `def` do?", ["source: notebook", "type: technical"],
     "It defines a new function", "It deletes the variable `n`", "It defers execution until later", "It defaults to zero", 1),
    ("MC", "clause", "What kind of loop requires a test condition or diamond shape in a flowchart?", ["source: notebook", "type: technical"],
     "A repetition structure", "A sequential assignment", "A variable declaration", "A hardware print step", 1),
    ("MC", "single word or term", "What does the line-for-line translation of the diamond describe?", ["source: notebook", "type: technical"],
     "A loop test", "A variable type", "A syntax error", "A data structure", 1),
    ("MC", "single word or term", "What is the term for `n` in `compute_factorials(n)`?", ["source: notebook", "type: technical"],
     "An input parameter", "A loop test variable", "An accumulator", "An output printer", 1),
    ("MC", "clause", "What is the outcome of passing a string to `print()`?", ["source: notebook", "type: technical"],
     "The string content is displayed", "The system shuts down", "The string is saved to disk", "The text is translated to French", 1),
    ("MC", "single word or term", "What shape typically represents a repetition back-arrow in a flowchart?", ["source: notebook", "type: technical"],
     "A loop", "A diamond", "A square", "An oval", 1),
    ("MC", "single word or term", "Which variable compounding each pass characterizes the factorial algorithm?", ["source: notebook", "type: technical"],
     "An accumulator", "A static constant", "A Boolean test", "An operation card", 1),
    ("MC", "clause", "How do you run code in Colab without installing Python?", ["source: notebook", "type: technical"],
     "It runs remotely in a browser", "It downloads a local virtual machine", "It writes a batch file", "It uses Javascript only", 1),
    ("MC", "clause", "What mathematical operation does a factorial algorithm perform repeatedly?", ["source: notebook", "type: technical"],
     "Multiplication", "Addition", "Subtraction", "Square roots", 1),
    ("MC", "clause", "What represents the execution of instructions in Colab?", ["source: notebook", "type: technical"],
     "Cells", "Pages", "Slides", "Sheets", 1),
    ("MC", "clause", "How are instructions organized in a function?", ["source: notebook", "type: technical"],
     "In a named, reusable block", "In random execution order", "As a single-use script only", "As immutable hardware logic", 1),
    ("MC", "single word or term", "What does 3! equal?", ["source: notebook", "type: technical"],
     "6", "3", "9", "12", 1),
    ("MC", "clause", "What happens to the running product in a factorial loop?", ["source: notebook", "type: technical"],
     "It is multiplied each pass", "It is cleared back to zero", "It is printed immediately", "It creates an infinite loop", 1),
    ("MC", "clause", "Why is `print` considered built-in?", ["source: notebook", "type: technical"],
     "It comes pre-installed with Python", "It requires external downloads", "It is only available online", "It was written by Babbage", 1),
     
    ("MR", "complete sentence", "Which two statements accurately describe Colab?", ["source: notebook", "type: conceptual"],
     "It runs code remotely in your browser.", "It provides access to AI pair-programmers.", "It requires an expensive physical server at your desk.", "It only supports block-based programming languages.", 1),
    ("MR", "complete sentence", "Which elements correspond to von Neumann architecture in Babbage's design?", ["source: notebook", "type: conceptual"],
     "The Mill acts as the CPU.", "The Store functions as system memory.", "The variable cards replace the need for math.", "The steam engine executes Python directly.", 1),
    ("MR", "complete sentence", "What operations are required to compute factorials?", ["source: notebook", "type: technical"],
     "Using an accumulator variable.", "A loop to iterate through values.", "Division by zero on each pass.", "Sorting the numbers in reverse.", 1),
    ("MR", "complete sentence", "In Python, which concepts apply to functions?", ["source: notebook", "type: technical"],
     "They are reusable blocks of code.", "They can accept input parameters like `n`.", "They run automatically without being invoked.", "They must always use a while loop inside.", 1),
    ("MR", "complete sentence", "What describes `compute_factorials` as implemented in the notebook?", ["source: notebook", "type: technical"],
     "It demonstrates algorithmic repetition.", "It is defined using the `def` keyword.", "It is part of the standard Python library.", "It computes logarithmic navigation tables.", 1),

    # CASE STUDY: CONCEPTUAL
    ("MC", "clause", "What was 'Lady Lovelace's Objection'?", ["source: case-study", "type: conceptual"],
     "Machines cannot originate anything", "Machines will eventually overpower humans", "Steam computers cannot execute loops", "Only men can write code", 1),
    ("MC", "clause", "What did Turing propose to replace the question 'Can machines think?'", ["source: case-study", "type: conceptual"],
     "The Imitation Game", "The Analytical Engine", "The Universality Theorem", "The Halting Problem", 1),
    ("MC", "single word or term", "Who did Lovelace translate her Notes from?", ["source: case-study", "type: conceptual"],
     "Luigi Menabrea", "Charles Babbage", "Alan Turing", "Mary Shelley", 1),
    ("MC", "clause", "Which mathematical sequence did Lovelace detail in Note G?", ["source: case-study", "type: conceptual"],
     "The Bernoulli numbers", "The Fibonacci sequence", "The prime numbers", "The factorials", 1),
    ("MC", "clause", "To Lovelace, what constituted the 'original' work of computing?", ["source: case-study", "type: conceptual"],
     "Designing the algorithmic rules", "Building the brass engine", "Punching the jacquard cards", "Executing the operations", 1),
    ("MC", "clause", "What is a universal machine?", ["source: case-study", "type: conceptual"],
     "A machine that can simulate any other machine", "A machine designed only for Bernoulli numbers", "A mechanical calculator powered by steam", "A physical loop of infinite paper", 1),
    ("MC", "clause", "Why did Turing think machines surprise us?", ["source: case-study", "type: conceptual"],
     "We cannot predict the consequences of complex rules", "They learn to break our rules", "They possess a human soul", "They randomly alter their data", 1),
    ("MC", "clause", "How does a Turing test judge if a machine is 'thinking'?", ["source: case-study", "type: conceptual"],
     "If a human cannot distinguish it from a human player", "If it solves equations faster than a human", "If it originates new mathematics", "If it translates French perfectly", 1),
    ("MC", "single word or term", "What term describes a finite list of unambiguous steps?", ["source: case-study", "type: conceptual"],
     "An algorithm", "A heuristic", "A processor", "An Engine", 1),
    ("MR", "complete sentence", "Which details apply to Turing's universal machine concept?", ["source: case-study", "type: conceptual"],
     "It relies on the idea that rules can be stored as data.", "It implies one machine can execute any computable program.", "It requires a different physical machine for each problem.", "It was proposed after World War II.", 1)
]

for idx, qa in enumerate(qa_data):
    q_type, a_style, prompt, tags, c1, c2, c3, c4, correct_pos = qa
    choices = [
        {"text": c1, "correct": correct_pos == 1},
        {"text": c2, "correct": correct_pos == 2},
        {"text": c3, "correct": correct_pos == 3},
        {"text": c4, "correct": correct_pos == 4},
    ]
    if q_type == "MR":
        # MR implies first two are correct conceptually from our manual setup.
        choices[0]["correct"] = True
        choices[1]["correct"] = True
        choices[2]["correct"] = False
        choices[3]["correct"] = False
        
    quiz["questions"].append({
        "question_type": q_type,
        "answer_style": a_style,
        "prompt": prompt,
        "answer_explanation": "",
        "points": "",
        "tags": tags,
        "choices": choices
    })

with open("perrusall_quizzes/sources/chapter-01-hardware-lovelace.quiz.json", "w", encoding="utf-8") as f:
    json.dump(quiz, f, indent=2)

print("Created quiz!")
