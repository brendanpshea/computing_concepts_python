import json

quiz = {
  "title": "Chapter 3 - Pseudocode, Flowcharts & Hopper's Bargain",
  "shuffle_answers": True,
  "questions": []
}

qa_data = [
    # CASE STUDY: CONCEPTUAL
    ("MC", "single word or term", "Who built the first working compiler?", ["source: case-study", "type: conceptual"],
     "Grace Hopper", "Alan Turing", "Charles Babbage", "Carver Mead", 1),
    ("MC", "clause", "What was the primary function of Hopper's A-0 compiler?", ["source: case-study", "type: conceptual"],
     "It translated symbolic language into machine instructions", "It checked Python code for syntax errors", "It automatically physically punched paper tape", "It calculated ballistics tables manually", 1),
    ("MC", "clause", "What does 'abstraction' mean in the context of computer science history?", ["source: case-study", "type: conceptual"],
     "Hiding complex machine operations behind simpler language layers", "Translating code back into physical hardware components", "Refusing to use visual flowcharts", "Writing code exclusively in binary logic", 1),
    ("MC", "clause", "What was COBOL designed to do?", ["source: case-study", "type: conceptual"],
     "Serve as a standard language for business data processing", "Train large language models on public source code", "Operate the Mark I mechanical computer", "Replace Python entirely", 1),
    ("MC", "clause", "Which issue did the Y2K bug highlight about abstraction?", ["source: case-study", "type: conceptual"],
     "Programmers had forgotten the lowest code layers that ran critical systems", "All modern compilers had a hidden hardware flaw", "LLMs were hallucinating fake library packages", "Mechanical moths still existed in server rooms", 1),
    ("MC", "clause", "According to Hopper, why was building a compiler necessary?", ["source: case-study", "type: conceptual"],
     "So ordinary technical workers could program without learning machine code", "So women could exclusively dominate the programming field", "To make computers run faster physically", "To prevent hardware bugs like moths from spreading", 1),
    ("MC", "clause", "What did Edsger Dijkstra argue about hiding the machine from the programmer?", ["source: case-study", "type: conceptual"],
     "It makes some kinds of errors invisible and impossible to diagnose", "It allows programs to run infinitely fast", "It permanently solves the problem of security flaws", "It is the only morally correct way to write software", 1),
    ("MC", "clause", "How does a compiler fundamentally differ from a Large Language Model (LLM)?", ["source: case-study", "type: conceptual"],
     "A compiler translates deterministically, while an LLM guesses statistically", "A compiler requires an internet connection to run", "An LLM writes only assembly language", "A compiler cannot translate Python code", 1),

    ("MR", "complete sentence", "Which components are characteristic of early programming (1940s)?", ["source: case-study", "type: conceptual"],
     "Code was heavily hand-translated into physical instructions.", "Operations were closely tied to physical machine architecture.", "Compilers automatically fixed logical errors.", "Visual drag-and-drop interfaces were standard.", 1),
    ("MR", "complete sentence", "What are the core arguments of the Labor Reply regarding abstraction?", ["source: case-study", "type: conceptual"],
     "Productivity tools change who does the work and on what terms.", "Technological shifts altered the gender demographics of the field.", "Abstraction creates perfectly equitable workplaces immediately.", "New compilers always guarantee higher wages for all workers.", 1),

    # NOTEBOOK: CONCEPTUAL
    ("MC", "single word or term", "What is an algorithm?", ["source: notebook", "type: conceptual"],
     "A precise sequence of executable steps", "A specific programming language like Python", "A hardware component connecting memory and CPU", "A random guess at a mathematical problem", 1),
    ("MC", "clause", "What should you do before translating an algorithm into code?", ["source: notebook", "type: conceptual"],
     "Pin it down in plain words and a picture", "Memorize all Python syntax rules", "Create a new variable named crowns", "Delete all floats from memory", 1),
    ("MC", "clause", "Which definition accurately describes a variable?", ["source: notebook", "type: conceptual"],
     "A labeled box that holds one value at a time", "A mathematical constant that never changes", "A built-in Python math function", "A flowchart diamond indicating choice", 1),
    ("MC", "clause", "What does a variable do when it receives a new assignment?", ["source: notebook", "type: conceptual"],
     "It forgets its old value entirely", "It mathematically adds the new value to the old", "It crashes the program if the type changes", "It copies the value to a secondary box", 1),
    ("MC", "clause", "In programming, what is the role of an expression?", ["source: notebook", "type: conceptual"],
     "It computes and evaluates to a value", "It acts as a complete executable instruction", "It only prints output to the screen", "It permanently deletes unused variables", 1),
    ("MC", "single word or term", "What dictates the operations allowed on a value?", ["source: notebook", "type: conceptual"],
     "Its data type", "The variable name", "The length of the code", "The CPU architecture", 1),
    ("MC", "clause", "Why is `\"42\"` different from `42` in Python?", ["source: notebook", "type: conceptual"],
     "Quotes mean the value is text, not a number", "Quotes make the number negative", "Quotes indicate a floating-point value", "Quotes tell Python to compute it faster", 1),
    ("MC", "clause", "How does a Python `float` visually differ from an `int`?", ["source: notebook", "type: conceptual"],
     "It contains a lone decimal point", "It is wrapped in quotation marks", "It has a negative sign in front", "It requires two assignment operators", 1),

    ("MR", "complete sentence", "Which elements are fundamental characteristics of an algorithm?", ["source: notebook", "type: conceptual"],
     "The steps are unambiguous and repeatable.", "A single problem can have multiple possible algorithms.", "They must be written exclusively in Python.", "They inherently require electronic hardware to run.", 1),
    ("MR", "complete sentence", "Which facts about the assignment operator (=) are correct?", ["source: notebook", "type: conceptual"],
     "The right side computes entirely before storing.", "Values flow exclusively from right to left.", "It tests whether two numbers are mathematically equal.", "It allows a box to hold two simultaneous values.", 1),

    # NOTEBOOK: TECHNICAL
    ("MC", "single word or term", "What symbol is used for the assignment operator?", ["source: notebook", "type: technical"],
     "`=`", "`==`", "`<-`", "`:`", 1),
    ("MC", "clause", "In `total = crowns - spent`, which part executes first?", ["source: notebook", "type: technical"],
     "Python computes `crowns - spent`", "Python creates the `total` variable", "Python prints the output", "Python stops the execution", 1),
    ("MC", "single word or term", "What type is `\"Mirabel\"`?", ["source: notebook", "type: technical"],
     "`str`", "`int`", "`float`", "`bool`", 1),
    ("MC", "single word or term", "What type is `3.14`?", ["source: notebook", "type: technical"],
     "`float`", "`int`", "`str`", "`bool`", 1),
    ("MC", "single word or term", "What type is `False`?", ["source: notebook", "type: technical"],
     "`bool`", "`str`", "`float`", "`int`", 1),
    ("MC", "single word or term", "What type is `100`?", ["source: notebook", "type: technical"],
     "`int`", "`float`", "`str`", "`bool`", 1),
    ("MC", "single word or term", "What operator computes integer floor division?", ["source: notebook", "type: technical"],
     "`//`", "`%`", "`/`", "`**`", 1),
    ("MC", "single word or term", "What operator computes the division remainder?", ["source: notebook", "type: technical"],
     "`%`", "`//`", "`/`", "`**`", 1),
    ("MC", "single word or term", "What built-in function returns the absolute value?", ["source: notebook", "type: technical"],
     "`abs()`", "`max()`", "`min()`", "`round()`", 1),
    ("MC", "single word or term", "What built-in function finds the largest in a set of numbers?", ["source: notebook", "type: technical"],
     "`max()`", "`min()`", "`abs()`", "`len()`", 1),
    ("MC", "single word or term", "If you evaluate `10 / 5`, what type is returned?", ["source: notebook", "type: technical"],
     "`float`", "`int`", "`str`", "`bool`", 1),
    ("MC", "single word or term", "What does `347 // 100` evaluate to?", ["source: notebook", "type: technical"],
     "3", "47", "3.47", "300", 1),
    ("MC", "single word or term", "What does `347 % 100` evaluate to?", ["source: notebook", "type: technical"],
     "47", "3", "3.47", "0", 1),
    ("MC", "clause", "What does a line of code like `spent = 70` represent?", ["source: notebook", "type: technical"],
     "A complete statement", "A raw operand", "A flowchart diamond", "A Boolean condition", 1),
    ("MC", "single word or term", "In `7 > 3`, what are the numbers 7 and 3?", ["source: notebook", "type: technical"],
     "Operands", "Variables", "Operators", "Statements", 1),
    ("MC", "clause", "What will `type(\"42\")` output?", ["source: notebook", "type: technical"],
     "`<class 'str'>`", "`<class 'int'>`", "`<class 'float'>`", "`<class 'bool'>`", 1),
    ("MC", "single word or term", "What does `round(3.14159, 2)` output?", ["source: notebook", "type: technical"],
     "3.14", "3", "3.1", "4", 1),
    ("MC", "single word or term", "What does `abs(-15)` evaluate to?", ["source: notebook", "type: technical"],
     "15", "-15", "0", "1.5", 1),

    ("MR", "clause", "Which expressions evaluate to integer types?", ["source: notebook", "type: technical"],
     "`347 // 100`", "`347 % 100`", "`10 / 5`", "`3.0 + 2.0`", 1),
    ("MR", "clause", "Which operations will output a float?", ["source: notebook", "type: technical"],
     "`10 / 2`", "`round(3.14159, 2)`", "`5 % 2`", "`10 // 3`", 1)
]


for idx, qa in enumerate(qa_data):
    q_type, a_style, prompt, tags, c1, c2, c3, c4, correct_pos = qa
    choices = [
        {"text": f"<code>{c1}</code>" if "`" in c1 else c1, "correct": correct_pos == 1},
        {"text": f"<code>{c2}</code>" if "`" in c2 else c2, "correct": correct_pos == 2},
        {"text": f"<code>{c3}</code>" if "`" in c3 else c3, "correct": correct_pos == 3},
        {"text": f"<code>{c4}</code>" if "`" in c4 else c4, "correct": correct_pos == 4},
    ]
    
    # Strip the backticks internally since we are wrapping in <code> tags if present
    for choice in choices:
        choice["text"] = choice["text"].replace("`", "")

    if q_type == "MR":
        choices[0]["correct"] = True
        choices[1]["correct"] = True
        choices[2]["correct"] = False
        choices[3]["correct"] = False
        
    import re
    prompt_fixed = prompt
    # Replace pairs of backticks with <code>...</code>
    prompt_fixed = re.sub(r"`([^`]+)`", r"<code>\1</code>", prompt_fixed)
    
    quiz["questions"].append({
        "question_type": q_type,
        "answer_style": a_style,
        "prompt": prompt_fixed,
        "answer_explanation": "",
        "points": "",
        "tags": tags,
        "choices": choices
    })

with open("perrusall_quizzes/sources/chapter-03-flowcharts-compilers.quiz.json", "w", encoding="utf-8") as f:
    json.dump(quiz, f, indent=2)

print("Created quiz!")
