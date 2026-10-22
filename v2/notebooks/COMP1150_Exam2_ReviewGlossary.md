# COMP 1150 — Exam 2 Review Glossary

*Chapters 4–6 and Case Studies 4–6. No definition uses the word it defines, so you can cover the left column and quiz yourself.*

---

## Chapter 4 — Control Flow & Functions

### Key Concepts

| Term | Definition |
|---|---|
| **Sequence** | The simplest control structure: steps run one after another, in order. |
| **Selection** (conditional) | Choosing between paths: code that runs only when a test comes out `True` (in Python, `if` / `elif` / `else`). |
| **Iteration** | Repeating a block of code (with `while` or `for`). Also means one single pass through that block. |
| **Structured program theorem** | Böhm & Jacopini's 1966 proof that sequence, selection, and iteration are enough to express any algorithm, which made the old jump-anywhere `goto` command unnecessary. |
| **Nesting** (nested decision / nested loop) | Placing one `if` or repeating block inside another; indentation shows the levels. With two repeating blocks, the inner one runs completely for each outer pass, so the total passes multiply (2 nights × 3 children = 6). |
| **Short-circuit** | Python stops checking an `and` / `or` as soon as the answer is settled: `False and …` is already `False`, and `True or …` is already `True`. |
| **Infinite loop** | Repetition that never ends because nothing inside it moves the condition toward `False`, such as a counter that never changes. |
| **Loop variable** | The name a `for` statement automatically fills with the next item on each pass (`child` in `for child in roster`). You never update it yourself. |
| **Accumulator** | A running total: set it up before the repetition (`total = 0`), update it on each pass, and use it afterward. Products start at `1` instead of `0`. |
| **Function** | A named, reusable block of code, created with `def`, that takes inputs and can hand back a result. Defining it doesn't run it; calling it does. |
| **Parameter / argument** | The placeholder name in a definition / the actual value supplied in a call. In `def f(x)`, `x` is the first kind; in `f(5)`, `5` is the second. |
| **Scope** | Where a name can be seen. Names created inside a function are *local*: they disappear when it finishes and can't be used outside it (`NameError`). |
| **Decomposition** (top-down design) | Breaking a big problem into small, named, separately testable pieces (usually functions) until each is easy, then combining them back up. |
| **DRY** (Don't Repeat Yourself) | Write each rule once, in one function, and call it wherever it's needed instead of copy-pasting. That gives you one place to fix bugs. |
| **Edge case** | An extreme or unusual input (empty list, zero, a negative, a boundary value, an unexpected status) that exposes bugs that normal inputs hide. |

: Chapter 4 key concepts and their definitions.

### Python Commands & Syntax

| Term | Definition |
|---|---|
| **`if` / `elif` / `else`** | Checks conditions top to bottom and runs only the *first* branch that is `True`; the final catch-all has no condition. Each line ends with a colon and is followed by an indented block. |
| **`and` / `or` / `not`** | `True` only when both sides are `True` / `True` when at least one side is `True` / flips a `True`–`False` value. Python checks the flip first, then "both," then "at least one." Use parentheses when unsure. |
| **`while` loop** | Repeats a block as long as its condition stays `True`. Use it when you don't know ahead of time how many passes you'll need. A safe one has three parts: set up, test, progress. |
| **`for` loop** | Steps through each item of a list or range, running the block once per item. Use it when you know exactly what to step through. |
| **`range(a, b)`** | Produces the whole numbers from `a` up to *but not including* `b`, so 1 to 5 gives 1, 2, 3, 4. To get 1 through `n`, use `(1, n + 1)`. |
| **`break` / `continue`** | Leave the repetition immediately / skip the rest of this pass and jump to the next one. Usually guarded by an `if`. |
| **`return`** | Hands one value back to the caller and ends the function. It is different from `print`, which only displays text on screen. A function without one gives back `None`. |
| **Default value** (`b=3` in a definition) | A fallback, written into the definition, that a parameter uses whenever the caller leaves it out. Parameters that have one must come after parameters that don't. |
| **Keyword argument** (`f(children=10)`) | Passing an input *by name* in the call, so the order no longer matters and the call reads like a sentence. |
| **Docstring** (`"""…"""`) | A triple-quoted, one-sentence description placed as the first line inside a function, saying what it does. `help()` displays it. |

: Chapter 4 Python commands and syntax, with their definitions.

### Case Study 4 — The Therac-25

| Term | Definition |
|---|---|
| **Race condition** | A bug where the outcome depends on the *timing* of two tasks that the programmer assumed would always happen in a fixed order. On the Therac-25, fast typists could finish an edit before the 8-second machine setup, so the beam fired at full strength. |
| **Integer overflow** | When a number grows too big for its storage and wraps around: a one-byte counter goes from 255 back to 0. Because of this, the Therac-25 skipped a safety check every 256th keypress. |
| **Hardware interlock** | A physical safety device that blocks a dangerous action no matter what the software says. The older Therac-20 had them; the Therac-25 removed them and trusted software alone. |
| **Reuse fallacy** | The mistaken belief that code is proven safe just because it ran without trouble before. The Therac-20 code only looked safe because physical safety devices had been backing it up. |
| **Programmer-blame argument** | The position that whoever wrote the faulty lines of code is responsible for the deaths. |
| **Systems reply** | Nancy Leveson's position that accidents in complex setups come from many interacting decisions (safety devices removed, no independent review, cryptic error messages), so no single coder is "the cause." |
| **Accountability objection** | The response that even when harm has many causes, specific people still made specific decisions (removing safety checks, denying injury reports) and must answer for them. A spread-out cause still has people responsible for it. |

: Case Study 4 (Therac-25) key terms and their definitions.

---

## Chapter 5 — Collections & Abstract Data Types

### Key Concepts

| Term | Definition |
|---|---|
| **List** | An ordered, changeable collection written with square brackets: `["cape", "fangs"]`. Use it when order matters and the contents will change. |
| **Tuple** | An ordered collection that can't be changed once built, written with round brackets: `("Harker", 178, "Hunter", 50)`. Use it for fixed-shape records. |
| **Dictionary** | A collection of labeled entries, written `{"domino mask": 5.00}`. Hand it a label and it jumps straight to the stored data. Use it to look things up by name or ID. |
| **Set** | An unordered collection with no duplicates, written with curly braces but no colons: `{"Hyde", "Mina"}`. Good for membership, uniqueness, and overlap. Careful: `{}` makes an empty *dictionary*, not an empty one of these. |
| **Mutable / immutable** | Can be changed after it's created (lists, dictionaries, sets) / locked once created (tuples, strings, numbers). |
| **Index** | An item's numbered position, starting at **0**. Negative numbers count back from the end, so `[-1]` is the last item. |
| **Slice** | A run of items pulled out with `[start:stop]`, where `stop` is *not* included. It always produces a new list and leaves the original alone. |
| **Aliasing** | Two names pointing at the very same list, so a change made through one shows up through the other. Writing `b = a` causes it; it does *not* make a copy. |
| **Unpacking** | Assigning the parts of a tuple to several names in one line: `name, height, costume, deposit = client`. This is also how a function seems to "hand back two things." |
| **Key–value pair** | One dictionary entry: a unique label you look things up by (left of the colon) and the data stored under it (right of the colon). |
| **Hashing** | Turning a lookup label into a number that says exactly which "shelf" holds the data. It is why dictionaries and sets find things fast without scanning, and why their labels must be immutable. |
| **List of dictionaries** | The standard shape of real-world data: one record per row, one labeled field per column. You read it in two steps: `ball[0]["name"]`. |
| **Comprehension** | A one-line shortcut for building a new list or dictionary from an old one: `[m + 2 for m in sleeves]`. You can add an `if` to keep only some items. |
| **Abstract data type (ADT)** | A description of *what* a collection promises to do (its operations), kept separate from *how* it stores its contents. For example, a waiting line that promises *add*, *next*, and *size*. |
| **Interface** | The operations something promises: their names, inputs, and outputs. Other code should rely only on this "promise." |
| **Implementation** | The actual storage and code behind a promise, such as a Python list doing the work behind a waiting line. It can be swapped out without breaking code that relies only on the promise. |
| **Queue** | A first-in, first-out (FIFO) line: items join at the back and leave from the front (`.append()` to add, `.pop(0)` to serve). |

: Chapter 5 key concepts and their definitions.

### Python Commands & Syntax

| Term | Definition |
|---|---|
| **`.append(x)` / `.remove(x)` / `.pop(i)`** | Add `x` to the end / delete the first item equal to `x` (error if it's missing) / take out the item at position `i` and hand it back (the last item if no position is given). |
| **`.copy()`** | Makes a new, independent list with the same contents, which is the fix for aliasing. `list(a)` and `a[:]` do the same job. |
| **`.get(key, default)`** | Safe dictionary lookup: hands back the stored data if the label exists, and otherwise gives `None` (or the fallback you chose) instead of crashing. |
| **`.items()`** | Hands over each (label, data) pair of a dictionary, so you can walk through them with two names: `for name, price in masks…`. |
| **`in`** | A `True`/`False` membership check: is this item (or dictionary label) present? It's fast for sets and dictionaries and slower for lists, which must be scanned. |
| **`sorted()` vs. `.sort()`** | The first hands back a *brand-new* ordered list and leaves the original alone; the second reorders the list itself and hands back nothing. `reverse=True` puts the largest first. |
| **Sort key** (`key=`) | The rule that decides what items are ordered *by*, such as ordering (mask, price) pairs by price instead of by name. |
| **Intersection** (`a & b`) | The items found in *both* sets. |
| **Union** (<code>a &#124; b</code>) | Every item found in *either* set. |
| **Difference** (`a - b`) | The items in the first set but *not* the second. |
| **`None`** | Python's special "nothing here" value. A function without a `return` hands it back, and `.get()` gives it for a missing label. |

: Chapter 5 Python commands and syntax, with their definitions.

### Case Study 5 — How We Represent People

| Term | Definition |
|---|---|
| **Schema** | The structure a system uses to store information: which fields exist, their types, and what each field may hold. The system can't remember anything it has no place for. |
| **Enum** | A field that only accepts choices from a fixed menu (e.g., `"male"`, `"female"`, `"other"`). Anything not on the menu can't be stored. |
| **Lossy (one-way) conversion** | Simplifying stored data in a way that throws information away for good. Once a person's name parts are flattened into a single string, you can never recover which part was the given name. |
| **Training set** | The labeled collection of examples a machine-learning model learns from. Its labels become the *only* categories the model can ever output. |
| **Exception path** | The side route (manual review, ID checks, support tickets) for people the main design doesn't fit. The debate is whether it is a fair fix or a hidden burden. |
| **Universalist argument** | The position that a design should fit the majority cleanly and handle unusual people with workarounds, because every extra field or option adds cost for everyone. |
| **Pluralist reply** | The response that workarounds aren't neutral: their costs fall again and again on the same groups. Choosing how to store people is really choosing who the system is built for. |

: Case Study 5 (How We Represent People) key terms and their definitions.

---

## Chapter 6 — Modules & Object-Oriented Programming

### Key Concepts

| Term | Definition |
|---|---|
| **Module** | A file of Python code you can bring into another file. Python ships with hundreds of them, ready to use, in its *standard library* (`math`, `random`, `datetime`). Write code once and use it everywhere. |
| **Namespace** | The "which home does this belong to?" idea. In `math.pi`, the dot says `pi` lives inside `math`, so it won't clash with a `pi` you made yourself. |
| **Object-oriented programming (OOP)** | A style (paradigm) of organizing code into bundles that own both their data *and* the behavior that acts on it. This is unlike *procedural* code, where separate functions act on passive data. |
| **Class** | A blueprint describing the data and methods that every thing built from it will have (e.g., `Citizen`). Names use CapWords by convention. |
| **Object** (instance) | One specific thing built from a blueprint, holding its own data: `elaine = Citizen(…)`. Changing one doesn't change another. |
| **Attribute** | A piece of data stored on an object. It is set with `self.name = name` and read back with a dot: `elaine.name`. |
| **Method** | A function defined inside a class. It acts on that object's data, always takes `self` first, and is called with a dot: `elaine.pay(20)`. |
| **Encapsulation** | Bundling data with the methods that act on it, and guarding that data so outside code goes through those methods. By convention, a leading underscore (`_pin`) means "internal, don't touch." |
| **Inheritance** | Building a specialized *child* class on top of a general *parent* class, so the child automatically gets the parent's attributes and methods. Written `class Knight(Guard):`. It models an "is-a" relationship. |
| **Override** | Giving a child class its own version of a method with the same name as the parent's. The child's version wins for child objects. |
| **Polymorphism** | Greek for "many shapes": one method name that does the right thing for each kind of object. Calling `.patrol()` on a mixed list of guards and knights runs each one's own version, with no `if` needed. |
| **Composition** | Building an object out of other objects it holds, which models a "has-a" relationship. A `Squad` *has* guards rather than *being* one. It's more flexible, because parts can be swapped while the program runs. |
| **Noun/verb heuristic** | A design starting trick: in a plain-English description of the problem, the *things* become candidate classes and attributes, and the *actions* become candidate methods. |
| **Cohesion** | How focused a class is on one clear job. The goal is *high*: a `Package` class should only know about packages. |
| **Coupling** | How tangled classes are with each other. If changing one forces you to rewrite another, they're tight. The goal is *low*. |
| **Abstraction** | Hiding complicated details behind a simple surface, so you can use something without knowing how it works inside. A function you call without reading its code is a "black box" of this kind. |
| **Abstraction layer** | One level in a stack where each level hides the one below it: transistors → logic gates → machine code → Python → your classes. |
| **Forgetting `self.`** (bug) | Writing a bare `balance = …` inside a method creates a throwaway local name, so the object's real data never changes and the update quietly vanishes. |
| **Shared mutable class attribute** (bug) | Putting a list (`members = []`) at the top of the blueprint instead of inside `__init__` gives *every* object the same single list, so adding through one object shows up in all of them. |

: Chapter 6 key concepts and their definitions.

### Python Commands & Syntax

| Term | Definition |
|---|---|
| **`import module`** | Brings a whole file of tools into reach. You use its contents with a dot, e.g., `math.sqrt(144)`. |
| **`from module import name`** | Pulls one specific tool out of a file so you can use it bare, with no prefix: `choice(clients)` instead of `random.choice(clients)`. |
| **`__init__`** | The special setup method that runs automatically every time a new object is built. It stores the object's starting data, and you never call it by name. |
| **`self`** | The first parameter of every method. It stands for the particular object the method was called on, and Python fills it in automatically (`elaine.pay(20)` passes `elaine`). |
| **`__str__`** | A special method that returns the text shown when an object is printed, instead of `<… object at 0x…>`. |
| **`super()`** | Refers to the parent class so a child can reuse its code, e.g., running the parent's `__init__` before adding a new `rank`. |

: Chapter 6 Python commands and syntax, with their definitions.

### Case Study 6 — Was OOP a Mistake?

| Term | Definition |
|---|---|
| **Message passing** | Alan Kay's original picture of how objects interact: you send an object a request, and it decides for itself how to respond, like cells signaling each other. |
| **Liskov Substitution Principle** | The rule that if code works with a parent class, it must keep working when handed any child class in its place. A `Square` that ties its width and height together breaks this, so it shouldn't inherit from `Rectangle`. |
| **"Favor composition over inheritance"** | The design advice from the 1994 "Gang of Four" *Design Patterns* book: build objects from parts they *have*, not from parents they supposedly *are*. It became the slogan the OOP debate settled on. |
| **Kay argument** | The Smalltalk creator's claim that OOP's real core is hidden data and request-sending objects. On this view, the problems people blame on OOP come from the class-hierarchy-heavy version that C++ and Java made popular. |
| **Pragmatist reply** | Bjarne Stroustrup's position that a programming style should be judged by whether teams actually build and maintain working systems with it, and class-based OOP ran an era's banks, phones, and operating systems. |
| **Functional reply** | The critique from Joe Armstrong and Rich Hickey that the real bug is gluing *changeable* data to behavior. Shared state that keeps changing causes the hardest bugs, so programs should be built from unchanging values combined by composition. |

: Case Study 6 (Was OOP a Mistake?) key terms and their definitions.
