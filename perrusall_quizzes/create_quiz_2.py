import json

quiz = {
  "title": "Chapter 2 - Machine Architecture & The Silicon Shield",
  "shuffle_answers": True,
  "questions": []
}

qa_data = [
    # CASE STUDY: CONCEPTUAL
    ("MC", "single word or term", "Who founded TSMC?", ["source: case-study", "type: conceptual"],
     "Morris Chang", "Carver Mead", "Lynn Conway", "Gordon Moore", 1),
    ("MC", "clause", "What was TSMC's unique business model?", ["source: case-study", "type: conceptual"],
     "A pure-play foundry", "An integrated device manufacturer", "An OS designer", "A vacuum-tube maker", 1),
    ("MC", "clause", "What did the Mead-Conway revolution achieve?", ["source: case-study", "type: conceptual"],
     "It standardized VLSI design rules", "It invented the pure silicon wafer", "It created the working transistor", "It built the pure-play foundry", 1),
    ("MC", "single word or term", "What kind of company is Nvidia?", ["source: case-study", "type: conceptual"],
     "Fabless", "Foundry", "IDM", "Toolmaker", 1),
    ("MC", "single word or term", "Which company builds EUV lithography machines?", ["source: case-study", "type: conceptual"],
     "ASML", "TSMC", "SMIC", "Intel", 1),
    ("MC", "clause", "What is the 'silicon shield' theory?", ["source: case-study", "type: conceptual"],
     "Taiwan's chip dominance deters invasion", "A physical coating over transistors", "A firewall for fabless designs", "China's indigenous chip effort", 1),
    ("MC", "clause", "What did the U.S. export controls in 2022 aim to restrict?", ["source: case-study", "type: conceptual"],
     "High-end AI chips and tools", "All consumer electronics exports", "Domestic software development", "Access to open-source languages", 1),
    ("MC", "clause", "How did Huawei respond to the export controls in 2023?", ["source: case-study", "type: conceptual"],
     "With a domestic 7nm chip", "By purchasing a TSMC stake", "By quitting smartphone making", "By suing Carver Mead", 1),
        
    ("MR", "complete sentence", "Which elements defined the traditional IDM model?", ["source: case-study", "type: conceptual"],
     "One company designed the chip.", "The same company owned the fab.", "The company only built for others.", "The process used open-source hardware.", 1),
    ("MR", "complete sentence", "Which arguments support the Fragmentation Reply?", ["source: case-study", "type: conceptual"],
     "Controls fund indigenous rival capability.", "Controls fragment the supply chain.", "Controls have no economic blowback.", "Controls destroy all worldwide AI models.", 1),

    # NOTEBOOK: CONCEPTUAL
    ("MC", "clause", "What is the central purpose of machine architecture?", ["source: notebook", "type: conceptual"],
     "Translating algorithms into hardware operations", "Inventing new mathematical theorems", "Building better word processors", "Making internet connections faster", 1),
    ("MC", "single word or term", "Which base describes the binary number system?", ["source: notebook", "type: conceptual"],
     "Base-2", "Base-10", "Base-16", "Base-8", 1),
    ("MC", "clause", "What does a single bit represent?", ["source: notebook", "type: conceptual"],
     "A choice between two states, like on or off", "A complete English alphabet character", "A full color image pixel", "A floating-point decimal number", 1),
    ("MC", "clause", "What defines the von Neumann architecture?", ["source: notebook", "type: conceptual"],
     "Sequential instruction and data space", "Exclusively parallel GPU clusters", "Running entirely without transistors", "Hardware disjoint from human inputs", 1),
    ("MC", "single word or term", "Which component acts as the computer's 'brain' in the von Neumann model?", ["source: notebook", "type: conceptual"],
     "The CPU", "The Memory", "The I/O bus", "The Power Supply", 1),
    ("MC", "clause", "What characterizes volatile memory?", ["source: notebook", "type: conceptual"],
     "Contents vanish without power", "Contents stay on hard drives", "It executes mathematical arithmetic", "It isolates software bugs", 1),
    ("MC", "clause", "How does bit width impact software capabilities?", ["source: notebook", "type: conceptual"],
     "It ceilings memory and precision", "It sets motherboard visual colors", "It controls internet transfer speeds", "It governs the operating system", 1),
    ("MC", "clause", "What happens visually when you double the bit width from 8-bit to 16-bit?", ["source: notebook", "type: conceptual"],
     "The reach exponentially squares", "The hardware requires double electricity", "The computer requires a larger monitor", "The reach scales linearly", 1),
     
    ("MR", "complete sentence", "Which elements are part of the von Neumann bottleneck?", ["source: notebook", "type: conceptual"],
     "The processor computes faster than memory delivers data.", "The bus acts as a literal internal speed limit.", "Modern AI models completely bypass the von Neumann structure.", "The CPU cannot perform any arithmetic operations.", 1),
    ("MR", "complete sentence", "Which facts apply to Gordon Moore's 1965 observation?", ["source: notebook", "type: conceptual"],
     "It described the exponential doubling of chip transistors.", "It correctly predicted decades of global industry growth.", "It was a legally binding international engineering treaty.", "It stated that chips would become more expensive every year.", 1),
     
     # NOTEBOOK: TECHNICAL
    ("MC", "single word or term", "What does the <code>bin()</code> function do in Python?", ["source: notebook", "type: technical"],
     "Converts an integer to a binary string", "Binds two variables together", "Creates a new binary file", "Sorts a list of numbers", 1),
    ("MC", "clause", "What prefix indicates a binary literal in Python?", ["source: notebook", "type: technical"],
     "<code>0b</code>", "<code>0x</code>", "<code>0o</code>", "<code>0d</code>", 1),
    ("MC", "clause", "If you binary-shift `1` left by 8 places, what value do you get?", ["source: notebook", "type: technical"],
     "256", "8", "64", "128", 1),
    ("MC", "single word or term", "What operator performs a bitwise left-shift in Python?", ["source: notebook", "type: technical"],
     "<code><<</code>", "<code>>></code>", "<code>//</code>", "<code>**</code>", 1),
    ("MC", "clause", "What does <code>sys.getsizeof()</code> return?", ["source: notebook", "type: technical"],
     "The memory size of an object in bytes", "The physical dimensions of the hard drive", "The number of lines in a Python script", "The maximum integer allowed by the CPU", 1),
    ("MC", "clause", "In Python, what happens if an integer exceeds a traditional 64-bit limit?", ["source: notebook", "type: technical"],
     "Python automatically allocates more memory to hold it", "The program crashes with an overflow error", "The number loops back to zero", "The number converts to a float", 1),
    ("MC", "single word or term", "What function tells you the memory address of a variable?", ["source: notebook", "type: technical"],
     "<code>id()</code>", "<code>loc()</code>", "<code>mem()</code>", "<code>addr()</code>", 1),
    ("MC", "clause", "How are Python strings generally encoded in modern versions?", ["source: notebook", "type: technical"],
     "Using Unicode", "Using ASCII exclusively", "Using base-16 hexadecimal directly", "Using analog wave patterns", 1),
    ("MC", "clause", "What does the <code>ord()</code> function do?", ["source: notebook", "type: technical"],
     "Returns the Unicode code point of a given character", "Orders a list sequentially", "Converts a number to a Roman numeral", "Creates an ordinary dictionary", 1),
    ("MC", "clause", "What does <code>chr()</code> do?", ["source: notebook", "type: technical"],
     "Returns the character corresponding to a Unicode code point", "Changes the variable reference", "Checks the hardware architecture", "Clears the memory buffer", 1),
    ("MC", "clause", "What kind of numbering system uses 16 symbols?", ["source: notebook", "type: technical"],
     "Hexadecimal", "Decimal", "Binary", "Octal", 1),
    ("MC", "clause", "What prefix indicates a hexadecimal number in Python?", ["source: notebook", "type: technical"],
     "<code>0x</code>", "<code>0b</code>", "<code>0h</code>", "<code>16x</code>", 1),
    ("MC", "single word or term", "How many bits are in a byte?", ["source: notebook", "type: technical"],
     "8", "4", "16", "32", 1),
    ("MC", "clause", "If a memory space is 8 bits wide, how many unique addresses can it reach?", ["source: notebook", "type: technical"],
     "256", "8", "64", "16", 1),
    ("MC", "single word or term", "What library must you import to use <code>getsizeof()</code>?", ["source: notebook", "type: technical"],
     "<code>sys</code>", "<code>os</code>", "<code>math</code>", "<code>memory</code>", 1),
    ("MC", "clause", "Why do integers in Python take up more than just their raw bit space?", ["source: notebook", "type: technical"],
     "Python wraps them in objects with overhead metadata", "Python converts all integers to floating-point numbers", "The CPU requires 24 bits for the binary sign", "Python stores them twice for safety", 1),
    ("MC", "clause", "How do you define a function that calculates <code>2 ** n</code>?", ["source: notebook", "type: technical"],
     "Using the <code>def</code> keyword", "Using the <code>func</code> keyword", "Using a <code>for</code> loop", "Using the <code>class</code> keyword", 1),
    ("MC", "clause", "How does a computer represent colors visually?", ["source: notebook", "type: technical"],
     "As RGB tuples combining Red, Green, and Blue intensities", "As single continuous analog waves", "Using only black and white binary strings", "By running physical paint pixels through the CPU", 1),
     
    ("MR", "complete sentence", "Which Python expressions represent the number 15?", ["source: notebook", "type: technical"],
     "The decimal literal <code>15</code>.", "The hexadecimal literal <code>0xF</code>.", "The string <code>\"fifteen\"</code>.", "The binary expression <code>15b</code>.", 1),
    ("MR", "complete sentence", "Related to Unicode string behavior, which statements are true?", ["source: notebook", "type: technical"],
     "<code>ord('A')</code> returns the integer value 65.", "<code>chr(65)</code> returns the string 'A'.", "Strings in Python are limited to 256 Ascii characters.", "The <code>bin()</code> function converts a string to alphabetical order.", 1)
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

with open("perrusall_quizzes/sources/chapter-02-architecture-silicon.quiz.json", "w", encoding="utf-8") as f:
    json.dump(quiz, f, indent=2)

print("Created quiz!")
