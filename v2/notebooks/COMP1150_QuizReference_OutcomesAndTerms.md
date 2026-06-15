# COMP 1150 — Learning Outcomes & Key Terms

*Quiz/test reference. One section per chapter: learning outcomes, then key terms (no definitions).*

---

## Chapter 1 — What Is Computing?

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Define** an algorithm and explain why algorithms — not computers — are the central idea in computer science
- **Read** pseudocode and a simple flowchart, and translate between pseudocode and Python
- **Trace** a small Python program line by line and predict its output
- **Describe** how computing hardware evolved from mechanical gears (1840s) to integrated circuits (1960s) and what each generation made newly possible
- **Use** an AI assistant to draft or modify code, and verify the result before trusting it

### Key Terms
- Abstraction
- Accumulator
- Algorithm
- Analytical Engine
- Brute-force search
- Caesar cipher
- Dictionary
- ELIZA effect
- Flowchart
- Function
- Integrated circuit
- Large Language Model (LLM)
- List of dictionaries
- Modulo (`%`)
- Pattern matching
- Pseudocode
- Punch card
- Time-sharing
- Transistor
- Vacuum tube
- Verification

---

## Chapter 2 — Machine Architecture & The Silicon Shield

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Explain** how a transistor becomes a logic gate, and how logic gates combine to do arithmetic
- **Describe** the von Neumann architecture, including the control unit, ALU, registers, and the fetch–decode–execute cycle
- **Explain** the memory hierarchy and why caching exists
- **Convert** numbers between binary, decimal, and hexadecimal by hand
- **Represent** negative numbers using two's complement, and decode a two's-complement byte
- **Explain** how text, images, and sound are all stored as numbers
- **Identify** how a representation choice (like a fixed-size integer) can cause real bugs

### Key Terms
- Transistor
- Logic gate
- Truth table
- Half-adder
- ALU (Arithmetic Logic Unit)
- Control Unit
- Register
- Program Counter (PC)
- Instruction Register (IR)
- Bus
- von Neumann architecture
- Fetch–decode–execute cycle
- Memory hierarchy
- Cache (hit / miss)
- Locality
- Bit / Byte
- Binary (base 2)
- Hexadecimal (base 16)
- Two's complement
- Integer overflow
- Character encoding (ASCII / Unicode)
- Pixel
- Sampling
- Palette

---

## Chapter 3 — Pseudocode, Flowcharts & Python Basics

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Create** variables and recognize the four core data types (`int`, `float`, `str`, `bool`)
- **Build** expressions with arithmetic, comparison, and boolean operators
- **Format** output with f-strings, escape characters, and string methods
- **Convert** between types correctly and read input from a person
- **Write** clear pseudocode and read a flowchart
- **Follow** the workflow *problem → pseudocode → flowchart → Python* on a real problem
- **Trace** a short program by hand, and use AI to pressure-test a plan you wrote yourself

### Key Terms
- Algorithm
- Representation
- Abstraction
- Variable
- Assignment (`=`)
- Data type
- int / float
- str / bool
- Expression / statement
- Operator / operand
- Floor division (`//`) / modulo (`%`)
- Comparison operators
- Boolean operators
- Operator precedence
- Type casting
- Escape character
- f-string / format specifier
- String method
- Pseudocode
- Flowchart
- Trace
- Comment (`#`)

---

## Chapter 4 — Control Flow & Functions

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Write** conditional logic with `if` / `elif` / `else`, including nested decisions
- **Combine** conditions with `and`, `or`, and `not`
- **Repeat** work with `while` and `for` loops, and steer them with `break` and `continue`
- **Recognise** and avoid infinite loops
- **Decompose** a problem into functions with parameters, default values, and return values
- **Document** a function with a docstring, and call it with keyword arguments
- **Explain** variable scope — why a value inside a function stays inside
- **Test** your logic against edge cases before trusting it

### Key Terms
- Conditional
- `if` / `elif` / `else`
- Nested decision
- `and` / `or` / `not`
- Short-circuit
- `while` loop
- `for` loop
- Loop variable
- `range(a, b)`
- Iteration
- Infinite loop
- `break` / `continue`
- Accumulator
- Function
- Parameter / argument
- Default value
- Keyword argument

---

## Chapter 5 — Collections & Abstract Data Types

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Choose** the right Python collection — list, tuple, dict, or set — for a given task and justify the choice.
- **Use** indexing, slicing, key lookup, sorting, and set operations to read, update, and re-shape data.
- **Diagnose** an aliasing bug, where two names point at the same list.
- **Read and build nested data** — a list of dictionaries — the shape that almost every real dataset takes.
- **Rewrite** small loops as list and dictionary **comprehensions**.
- **Explain** the difference between an **abstract data type** (the promise) and its **implementation** (the storage), and implement a small ADT yourself.

### Key Terms
- Abstract Data Type (ADT)
- Aliasing
- Comprehension
- Copy
- Default value
- Dictionary
- Difference (sets)
- Immutable
- Implementation
- Index
- Interface
- Intersection (sets)
- Key
- List
- List of dictionaries
- Mutable
- `None`
- Set
- Slice
- Sort key
- Tuple
- Union (sets)
- Unpacking
- Value

---

## Chapter 6 — Modules & Object-Oriented Programming

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Import** code from Python's standard library and from your own files, and explain what a **module** and a **namespace** are.
- **Define** a class with `__init__`, create objects from it, and explain the difference between a **class** (the blueprint) and an **object** (a thing built from it).
- **Write** methods that use `self` to act on an object's own data, and explain what `self` refers to.
- **Use** inheritance and `super()` to build a specialized class on top of a general one, and **override** a method.
- **Explain** encapsulation and abstraction, and implement a small **abstract data type** as a class.
- **Spot** two classic OOP bugs: forgetting `self.`, and a mutable class attribute shared across every object.

### Key Terms
- Abstraction
- Abstraction layer
- Attribute
- Class
- Cohesion
- Composition
- Coupling
- Encapsulation
- `__init__`
- Inheritance
- Instance
- Method
- Module
- Namespace

---

## Chapter 7 — Searching, Sorting & How Long It Takes

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Perform** a **linear search** over a list and explain when it is the only option.
- **Perform** a **binary search** over a *sorted* list, and explain why the list must be sorted first.
- **Reason** informally about **running time** using Big-O names — `O(n)`, `O(log n)`, `O(n²)`, `O(n log n)` — to describe how work grows as data grows.
- **Hand-code** one simple sorting algorithm (selection sort) and **describe** how a faster one (merge sort) works.
- **Use** Python's built-in `sorted()` and `.sort()` with a `key=` function to sort numbers, strings, and objects.
- **Describe** a **Turing machine** as a thought experiment and say what it means for a problem to be **computable**.
- **Explain** the **halting problem** and what it means for a problem to be **undecidable**.
- **Discuss** **P vs. NP** as the cultural idea "easy to check, hard to solve," and connect these limits to what modern AI / LLMs can and cannot do *in principle*.

### Key Terms
- Algorithm
- Linear search
- Binary search
- Sentinel value
- Big-O notation
- `O(1)`, `O(log n)`, `O(n)`, `O(n log n)`, `O(n²)`
- Selection sort
- Merge sort
- Swap
- In-place
- Key function
- Turing machine
- Church–Turing thesis
- Computable
- Halting problem
- Undecidable
- P
- NP
- P vs. NP
- Intractable

---

## Chapter 8 — Software Engineering: SDLC, Git & AI-Assisted Development

### Learning Outcomes
By the end of this notebook, students will be able to:

- **Describe** the stages of the **software development life cycle (SDLC)** and explain why teams plan before they type.
- **Write** a clear **requirement** and **user story** for a feature.
- **Use** **git** to track changes, read a project's history, and recover an earlier version of your work — and **explain** how git is really used day-to-day through GitHub and your code editor.
- **Write** simple **tests** with `assert` to check that code is *correct*, not just that it *runs*.
- **Review** AI-generated code critically — finding bugs and judgment problems *before* they ship.
- **Explain** how software is actually built in 2026, when AI writes much of the code, and **discuss** who is responsible for it.

### Key Terms
- Software development life cycle (SDLC)
- Waterfall
- Agile
- Sprint
- Requirement
- User story
- Version control
- Git
- Repository (repo)
- Commit
- Staging area
- GitHub
- Branch
- Pull request (PR)
- Code review
- Test
- Assertion (`assert`)
- Decomposition
- Pure logic vs. I/O
- Spec
- Iterative development
- Regression
- Prompt
- Hallucination
- Accountability
