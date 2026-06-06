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
    ("MC", "single word or term", "What is the decimal value of the binary number <code>1010</code>?", ["source: notebook", "type: technical"],
     "10", "8", "12", "16", 1),
    ("MC", "single word or term", "What is the binary representation of the decimal number <code>13</code>?", ["source: notebook", "type: technical"],
     "<code>1101</code>", "<code>1011</code>", "<code>1110</code>", "<code>1001</code>", 1),
    ("MC", "single word or term", "What is the hexadecimal equivalent of the binary number <code>1111 1111</code>?", ["source: notebook", "type: technical"],
     "<code>FF</code>", "<code>EE</code>", "<code>11</code>", "<code>00</code>", 1),
    ("MC", "single word or term", "What is the decimal value of the hexadecimal number <code>1A</code>?", ["source: notebook", "type: technical"],
     "26", "24", "16", "32", 1),
    ("MC", "single word or term", "How many unique values can be represented by 4 bits?", ["source: notebook", "type: technical"],
     "16", "8", "4", "32", 1),
    ("MC", "clause", "In two's complement, what does the leftmost bit usually signify?", ["source: notebook", "type: technical"],
     "The mathematical sign of the number", "The magnitude of the exponent", "A parity check for errors", "The start of the data string", 1),
    ("MC", "single word or term", "What is the 8-bit two's complement representation of <code>-1</code>?", ["source: notebook", "type: technical"],
     "<code>1111 1111</code>", "<code>1000 0001</code>", "<code>0000 0001</code>", "<code>0111 1111</code>", 1),
    ("MC", "single word or term", "What is the decimal equivalent of the 8-bit two's complement binary number <code>1000 0000</code>?", ["source: notebook", "type: technical"],
     "-128", "-1", "128", "0", 1),
    ("MC", "single word or term", "If you binary-shift <code>0010</code> left by one position, what is the new decimal value?", ["source: notebook", "type: technical"],
     "4", "1", "8", "2", 1),
    ("MC", "single word or term", "What is the hexadecimal representation of decimal <code>255</code>?", ["source: notebook", "type: technical"],
     "<code>FF</code>", "<code>AA</code>", "<code>2F</code>", "<code>F0</code>", 1),
    ("MC", "single word or term", "Convert the hexadecimal number <code>10</code> to decimal.", ["source: notebook", "type: technical"],
     "16", "10", "2", "8", 1),
    ("MC", "single word or term", "What is the binary representation of the hexadecimal digit <code>C</code>?", ["source: notebook", "type: technical"],
     "<code>1100</code>", "<code>1010</code>", "<code>1110</code>", "<code>1011</code>", 1),
    ("MC", "single word or term", "What is the largest positive integer you can represent in 8-bit two's complement?", ["source: notebook", "type: technical"],
     "127", "255", "128", "256", 1),
    ("MC", "clause", "How do you find the two's complement of a binary number?", ["source: notebook", "type: technical"],
     "Invert all bits and add 1", "Reverse the order of the bits", "Change the leftmost bit to 0", "Subtract 1 and invert all bits", 1),
    ("MC", "single word or term", "Convert the unsigned binary <code>1101</code> to hexadecimal.", ["source: notebook", "type: technical"],
     "<code>D</code>", "<code>B</code>", "<code>C</code>", "<code>E</code>", 1),
    ("MC", "single word or term", "Convert the decimal <code>7</code> to a 4-bit binary string.", ["source: notebook", "type: technical"],
     "<code>0111</code>", "<code>1000</code>", "<code>0110</code>", "<code>0101</code>", 1),
    ("MC", "clause", "What happens if you add 1 to the largest positive number in two's complement?", ["source: notebook", "type: technical"],
     "It overflows to an incorrect negative number", "The CPU upgrades to a larger bit width", "The result stays exactly the same", "The system correctly represents the new positive number", 1),
    ("MC", "single word or term", "What is the decimal value of the unsigned binary number <code>1111</code>?", ["source: notebook", "type: technical"],
     "15", "16", "14", "8", 1),

    ("MR", "clause", "Which of the following are equal to decimal 12?", ["source: notebook", "type: technical"],
     "Hexadecimal <code>C</code>", "Binary <code>1100</code>", "Hexadecimal <code>A</code>", "Binary <code>1010</code>", 1),
    ("MR", "complete sentence", "Which statements about two's complement are correct?", ["source: notebook", "type: technical"],
     "It allows subtraction to be computed via addition.", "It has exactly one representation for the number zero.", "It reserves two distinct patterns for positive and negative zero.", "It only works to represent positive floating point values.", 1)
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
