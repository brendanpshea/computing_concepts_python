import random
import ipywidgets as widgets
from IPython.display import display, clear_output

# Utility Functions
def pretty_print_list(lst):
    if not lst:
        return ''
    elif len(lst) == 1:
        return str(lst[0])
    else:
        return ', '.join(str(item) for item in lst[:-1]) + ', and ' + str(lst[-1])

def array_contains(array, e):
    return e in array

def array_without_element(array, e):
    return [x for x in array if x != e]

def add_unique(array, e):
    if e not in array:
        array.append(e)
    return array

def add_all_unique(array1, array2):
    for e in array2:
        if e not in array1:
            array1.append(e)
    return array1

def arrays_equivalent(array1, array2):
    return set(array1) == set(array2)

def copy_array(array):
    return array.copy()

def random_int(less_than):
    return random.randrange(less_than)

def random_range(greater_than, less_than):
    return random.randint(greater_than, less_than)

def random_element(array):
    return random.choice(array)

def shuffle(array):
    random.shuffle(array)
    return array

def array_difference(array1, array2):
    return [e for e in array1 if e not in array2]

# Mythological Names
mythological_male_names = [
    'Zeus', 'Apollo', 'Osiris', 'Ra', 'Shiva', 'Vishnu', 'Odin', 'Thor',
    'Horus', 'Anubis', 'Kronos', 'Hercules', 'Ganesh', 'Poseidon', 'Krishna',
    'Hades', 'Ares', 'Rama', 'Yama', 'Atlas'
]

mythological_female_names = [
    'Athena', 'Isis', 'Hera', 'Aphrodite', 'Lakshmi', 'Parvati', 'Freya',
    'Amaterasu', 'Sita', 'Durga', 'Kali', 'Persephone', 'Gaia', 'Demeter',
    'Artemis', 'Sekhmet', 'Nephthys', 'Saraswati', 'Chang\'e', 'Nuwa'
]

def name_set():
    names = mythological_male_names + mythological_female_names
    random.shuffle(names)
    return names.copy()

# Islander Classes
class Islander:
    def __init__(self, name):
        self.name = name

    def match_statement_for(self, other):
        if other.is_knight():
            return Sympathetic(self, other)
        else:
            return Antithetic(self, other)

    def __str__(self):
        return self.name

class Knight(Islander):
    def is_knight(self):
        return True

    def statement_for(self, other):
        if other.is_knight():
            return Affirmation(self, other)
        else:
            return Accusation(self, other)

    def compound_statement_for(self, other):
        return Disjoint(self, other)

    def type(self):
        return "knight"

class Knave(Islander):
    def is_knight(self):
        return False

    def statement_for(self, other):
        if other.is_knight():
            return Accusation(self, other)
        else:
            return Affirmation(self, other)

    def compound_statement_for(self, other):
        return Joint(self, other)

    def type(self):
        return "knave"

# Statement Classes
class Statement:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.text = self.build_statement()

    def full_statement(self):
        return f"{self.source.name} says: \"{self.text}.\""

    def __str__(self):
        return self.full_statement()

class TypeStatement(Statement):
    def done(self, solver):
        has_target = self.target in solver.knights or self.target in solver.knaves
        has_source = self.source in solver.knights or self.source in solver.knaves
        return has_target and has_source

    def process(self, known, solver):
        if self.source == known or self.target == known:
            islanders = [self.source, self.target]
            islanders.remove(known)
            unknown = islanders[0]
            solver.reasoning.append(self.reasoning(known))
            if unknown.is_knight():
                add_unique(solver.knights, unknown)
            else:
                add_unique(solver.knaves, unknown)

    def solve(self, solver):
        solver.type_statements.append(self)

class Accusation(TypeStatement):
    def build_statement(self):
        options = [
            " is lying",
            " is a knave",
            " always lies",
            " never tells the truth",
            " lies",
            " is untruthful"
        ]
        return self.target.name + random_element(options)

    def reasoning(self, known):
        islanders = [self.source, self.target]
        islanders.remove(known)
        unknown = islanders[0]
        s = "All islanders will call a member of the opposite type a knave."
        s += f" So when {self.source} says that {self.target} is a knave, we know that "
        s += f"{self.target} and {self.source} are opposite types."
        s += f" Since {known.name} is a {known.type()}, then {unknown.name} is a {unknown.type()}."
        return s

class Affirmation(TypeStatement):
    def build_statement(self):
        options = [
            " is truthful",
            " is a knight",
            " always tells the truth",
            " never lies",
            " tells the truth"
        ]
        return self.target.name + random_element(options)

    def reasoning(self, known):
        islanders = [self.source, self.target]
        islanders.remove(known)
        unknown = islanders[0]
        s = "All islanders will call one of their same kind a knight."
        s += f" So when {self.source} says that {self.target} is a knight, we know that "
        s += f"{self.target} and {self.source} are the same type."
        s += f" Since {known.name} is a {known.type()}, then {unknown.name} is a {unknown.type()}."
        return s

class Sympathetic(Statement):
    def build_statement(self):
        options = [
            " is my type"
        ]
        return self.target.name + random_element(options)

    def reasoning(self):
        s = "A knight or a knave will say they are the same type as a knight."
        s += f" So when {self.source} says they are the same type as {self.target}, we know that "
        s += f"{self.target.name} is a knight."
        return s

    def solve(self, solver):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knights, self.target)

class Antithetic(Statement):
    def build_statement(self):
        options = [
            " is not my type"
        ]
        return self.target.name + random_element(options)

    def reasoning(self):
        s = "Both knights and knaves will say they are not the same type as a knave."
        s += f" So when {self.source} says they are a different type than {self.target}, we know that "
        s += f"{self.target.name} is a knave."
        return s

    def solve(self, solver):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knaves, self.target)

class Disjoint(Statement):
    def build_statement(self):
        self.text = self.target.name
        if self.target.is_knight():
            self.text += " is a knight "
        else:
            self.text += " is a knave "
        self.text += "or I am a knave"
        return self.text

    def reasoning(self):
        s = f"When {self.source} said '{self.text}',"
        s += f" we know {self.source.name} must be making a true statement."
        s += " (If it was false, this would make the speaker a knave, which would make the statement true, but knaves cannot make true statements.)"
        s += f" So, {self.source.name} is a knight and {self.target.name}"
        s += f" is a {self.target.type()}."
        return s

    def solve(self, solver):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knights, self.source)
        if self.target.is_knight():
            add_unique(solver.knights, self.target)
        else:
            add_unique(solver.knaves, self.target)

class Joint(Statement):
    def build_statement(self):
        self.text = self.target.name
        if self.target.is_knight():
            self.text += " is a knave "
        else:
            self.text += " is a knight "
        self.text += "and I am a knave"
        return self.text

    def reasoning(self):
        s = f"Because {self.source} said '{self.text}',"
        s += f" we know {self.source.name} is not making a true statement."
        s += " (If it was true, the speaker would be a knight claiming to be a knave, which cannot happen.)"
        s += f" Therefore, {self.source.name} is a knave and {self.target.name}"
        s += f" is a {self.target.type()}."
        return s

    def solve(self, solver):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knaves, self.source)
        if self.target.is_knight():
            add_unique(solver.knights, self.target)
        else:
            add_unique(solver.knaves, self.target)

# Puzzle Classes
class Puzzle:
    def __init__(self):
        self.islanders = None
        self.statements = None
        self.knaves = None
        self.knights = None
        self.islander_controllers = None

    def get_islanders(self):
        return self.islanders

    def get_statements(self):
        return self.statements

    def knave_names(self):
        return [knave.name for knave in self.knaves]

    def knight_names(self):
        return [knight.name for knight in self.knights]

    def __str__(self):
        return f"Puzzle knights [{pretty_print_list(self.knight_names())}] knaves: [{pretty_print_list(self.knave_names())}]"

class CompoundPuzzle(Puzzle):
    def __init__(self, names=None):
        super().__init__()
        self.puzzles = []
        self.knaves = []
        self.knights = []
        self.islanders = []
        self.islander_controllers = {}
        self.statements = []
        self.name_set = names

    def join(self, target):
        self.puzzles.append(target)
        self.knaves = add_all_unique(self.knaves, target.knaves)
        self.knights = add_all_unique(self.knights, target.knights)
        self.islanders = add_all_unique(self.islanders, target.islanders)
        self.statements = add_all_unique(self.statements, target.statements)

    def random_join(self, target):
        choice = random_int(2)
        if choice == 0:
            self.join_with_match(target)
        else:
            self.join_with_compound(target)

    def join_with_match(self, target):
        s = random_element(self.get_islanders())
        t = random_element(target.get_islanders())
        self.join(target)
        state = s.match_statement_for(t)
        self.statements.append(state)

    def join_with_compound(self, target):
        s = random_element(self.get_islanders())
        t = random_element(target.get_islanders())
        self.join(target)
        state = s.compound_statement_for(t)
        self.statements.append(state)

class SimplePuzzle(Puzzle):
    def __init__(self, count, names):
        super().__init__()
        self.count = count
        if count == 1:
            self.liar_count = 1
        elif count < 4:
            self.liar_count = random_int(count)
        else:
            self.liar_count = random_range(max(count // 2 - 1, 0), count - 2)
        self.knaves = []
        self.knights = []
        self.islanders = []
        self.islander_controllers = {}
        self.name_set = names if names else copy_array(mythological_male_names + mythological_female_names)
        for _ in range(self.liar_count):
            pos = random_range(0, len(self.name_set) - 1)
            islander = Knave(self.name_set.pop(pos))
            self.knaves.append(islander)
            self.islander_controllers[islander.name] = IslanderController(islander)
        for _ in range(self.liar_count, self.count):
            pos = random_range(0, len(self.name_set) - 1)
            islander = Knight(self.name_set.pop(pos))
            self.knights.append(islander)
            self.islander_controllers[islander.name] = IslanderController(islander)
        self.islanders = shuffle(self.knaves + self.knights)
        self.statements = self.generate_statements()

    def generate_statements(self):
        statements = []
        if len(self.islanders) < 2:
            return statements
        prev_source = None
        for target in self.islanders:
            remainders = array_without_element(self.islanders, target)
            if prev_source is not None:
                remainders = array_without_element(remainders, prev_source)
                if not remainders:
                    remainders = array_without_element(self.islanders, target)
            source = random_element(remainders)
            statements.append(source.statement_for(target))
            prev_source = source
        statements = prune_statements(statements)
        statements = join_connected_sets(self.islanders, statements)
        return shuffle(statements)

    def complete_with_match(self):
        if len(self.islanders) < 2:
            return
        source = random_element(self.islanders)
        remainders = array_without_element(self.islanders, source)
        nbrs = all_sources_and_targets(source, self.statements)
        left = array_difference(remainders, nbrs)
        if not left:
            target = random_element(remainders)
        else:
            target = random_element(left)
        self.statements.append(source.match_statement_for(target))
        shuffle(self.statements)

    def complete_with_compound(self):
        if len(self.islanders) < 2:
            return
        source = random_element(self.islanders)
        remainders = array_without_element(self.islanders, source)
        nbrs = all_sources_and_targets(source, self.statements)
        left = array_difference(remainders, nbrs)
        if not left:
            target = random_element(remainders)
        else:
            target = random_element(left)
        self.statements = remove_statement_with(source, target, self.statements)
        self.statements.append(source.compound_statement_for(target))
        shuffle(self.statements)

    def random_completion(self):
        choice = random_int(2)
        if choice == 0:
            self.complete_with_match()
        else:
            self.complete_with_compound()

# Solver Class
class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.reasoning = []
        self.type_statements = []
        self.knights = []
        self.knaves = []

    def solve(self):
        for statement in self.puzzle.statements:
            statement.solve(self)

        remaining_statements = self.type_statements.copy()

        while remaining_statements:
            next_remaining = remaining_statements.copy()
            for s in remaining_statements:
                if s.done(self):
                    next_remaining = array_without_element(next_remaining, s)
                    continue
                knave_copy = self.knaves.copy()
                for knave in knave_copy:
                    s.process(knave, self)
                if s.done(self):
                    next_remaining = array_without_element(next_remaining, s)
                    continue
                knight_copy = self.knights.copy()
                for knight in knight_copy:
                    s.process(knight, self)
            if arrays_equivalent(remaining_statements, next_remaining):
                break  # No progress, avoid infinite loop
            remaining_statements = next_remaining

        str_result = "\n".join(f"- {r}" for r in self.reasoning)
        str_result += "\n\nFor these reasons we know"
        if len(self.puzzle.knave_names()) == 0:
            str_result += " there were no knaves"
        elif len(self.puzzle.knave_names()) == 1:
            str_result += " the only knave was " + pretty_print_list(self.puzzle.knave_names())
        else:
            str_result += " the knaves were " + pretty_print_list(self.puzzle.knave_names())
        str_result += ", and"
        if len(self.puzzle.knight_names()) == 0:
            str_result += " there were no knights."
        elif len(self.puzzle.knight_names()) == 1:
            str_result += " the only knight was " + pretty_print_list(self.puzzle.knight_names()) + "."
        else:
            str_result += " the knights were " + pretty_print_list(self.puzzle.knight_names()) + "."
        self.validate()
        return str_result

    def validate(self):
        is_valid = arrays_equivalent(self.knights, self.puzzle.knights)
        is_valid = is_valid and arrays_equivalent(self.knaves, self.puzzle.knaves)
        if not is_valid:
            print("ERROR: automated solver did not find the complete solution")
            print("solver:", self)
            print("puzzle:", self.puzzle)
        else:
            pass  # The solver found the correct solution

    def __str__(self):
        return f"knights: {self.knights} knaves: {self.knaves}"

# PuzzleGenerator Class
class PuzzleGenerator:
    def __init__(self):
        self.puzzle = None

    def easy(self):
        choice = random_int(3)
        if choice == 0:
            self.easy0()
        elif choice == 1:
            self.easy1()
        else:
            self.easy2()

    def medium(self):
        choice = random_int(3)
        if choice == 0:
            self.medium0()
        elif choice == 1:
            self.medium1()
        elif choice == 2:
            self.medium2()

    def hard(self):
        choice = random_int(2)
        if choice == 0:
            self.hard0()
        elif choice == 1:
            self.hard1()

    def easy0(self):
        self.puzzle = SimplePuzzle(2, copy_array(name_set()))
        self.puzzle.complete_with_match()

    def easy1(self):
        self.puzzle = SimplePuzzle(2, copy_array(name_set()))
        self.puzzle.complete_with_compound()

    def easy2(self):
        self.puzzle = SimplePuzzle(3, copy_array(name_set()))
        self.puzzle.random_completion()

    def medium0(self):
        names = copy_array(name_set())
        basic = SimplePuzzle(3, names)
        basic1 = SimplePuzzle(1, names)
        basic.random_completion()
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.random_join(basic1)

    def medium1(self):
        names = copy_array(name_set())
        basic = SimplePuzzle(3, names)
        basic.complete_with_match()
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)

    def medium2(self):
        names = copy_array(name_set())
        basic = SimplePuzzle(1, names)
        basic1 = SimplePuzzle(3, names)
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.join_with_compound(basic1)

    def hard0(self):
        names = copy_array(name_set())
        basic = SimplePuzzle(3, names)
        basic2 = SimplePuzzle(3, names)
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.join_with_compound(basic2)

    def hard1(self):
        names = copy_array(name_set())
        basic = SimplePuzzle(3, names)
        basic2 = SimplePuzzle(3, names)
        basic.complete_with_match()
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.join_with_match(basic2)

    def controller(self):
        return IslandControllers(self.puzzle)

# Graph Functions
def prune_statements(statements):
    extras = []
    for e in statements:
        if e in extras:
            continue
        s = e.source
        t = e.target
        remainder = array_without_element(statements, e)
        for e1 in remainder:
            s1 = e1.source
            t1 = e1.target
            if s1 == t and t1 == s:
                extras.append(e1)
    return array_difference(statements, extras)

def join_connected_sets(islanders, statements):
    c_sets = connected_sets(islanders, islanders, statements, [], [])
    if len(c_sets) == 1:
        return statements
    joiner = c_sets[0][0]
    remaining_sets = array_without_element(c_sets, c_sets[0])
    new_statements = []
    for x in remaining_sets:
        joinee = x[0]
        new_statements.append(joinee.statement_for(joiner))
    return statements + new_statements

def connected_sets(islanders, complete_islanders, statements, set_list, so_far):
    connect1 = all_reachable(islanders[0], statements, [])
    add_all_unique(so_far, connect1)
    set_list.append(connect1)
    if arrays_equivalent(complete_islanders, so_far):
        return set_list
    remainder = array_difference(islanders, so_far)
    return connected_sets(remainder, complete_islanders, statements, set_list, so_far)

def all_reachable(islander, statements, list_so_far):
    reachable = list_so_far.copy()
    immediate_neighbours = all_sources_and_targets(islander, statements)
    reachable = add_all_unique(reachable, immediate_neighbours)
    if arrays_equivalent(reachable, list_so_far):
        return list_so_far
    for neighbour in immediate_neighbours:
        reachable = add_all_unique(reachable, all_reachable(neighbour, statements, reachable))
    return reachable

def all_sources_and_targets(islander, statements):
    list_islanders = []
    for e in statements:
        source = e.source
        target = e.target
        if islander == source:
            list_islanders.append(target)
        if islander == target:
            list_islanders.append(source)
    return list_islanders

def array_difference(array1, array2):
    return [e for e in array1 if e not in array2]

def remove_statement_with(islander1, islander2, statements):
    for e in statements:
        s = e.source
        t = e.target
        if (s == islander1 or s == islander2) and (t == islander1 or t == islander2):
            statements = array_without_element(statements, e)
            return statements
    return statements

# IslanderController and IslandControllers Classes
class IslanderController:
    def __init__(self, islander):
        self.islander = islander

class IslandControllers:
    def __init__(self, island):
        self.island = island

    def accusation_display(self):
        p = f"You have met a group of {len(self.island.islanders)} islanders."
        p += f" Their names are {pretty_print_list([str(islander) for islander in self.island.islanders])}.\n"
        s = "\n".join(statement.full_statement() for statement in self.island.get_statements())
        return p + "\n" + s

# Game Functions
def play_game():
    levels = ['Easy', 'Medium', 'Hard']
    level_index = 0
    puzzles_solved = 0

    # Variables to keep track of game state
    game_state = {'level_index': level_index, 'puzzles_solved': puzzles_solved}

    # Function to display the next puzzle
    def next_puzzle():
        clear_output(wait=True)
        level_index = game_state['level_index']
        puzzles_solved = game_state['puzzles_solved']

        if level_index >= len(levels):
            print("Congratulations! You have completed all levels!")
            return

        difficulty = levels[level_index]
        print(f"\nCurrent Level: {difficulty}")
        print(f"You need to solve 3 puzzles to advance to the next level.\n")

        # Generate puzzle
        generator = PuzzleGenerator()
        if difficulty == 'Easy':
            generator.easy()
        elif difficulty == 'Medium':
            generator.medium()
        elif difficulty == 'Hard':
            generator.hard()
        else:
            generator.easy()

        puzzle = generator.puzzle

        # Display the puzzle description
        controller = generator.controller()
        description = controller.accusation_display()
        print(description)

        # Create widgets for user to select roles
        print("\nWho do you think are Knights and Knaves?")
        islander_names = [islander.name for islander in puzzle.islanders]
        knight_checks = {}
        knave_checks = {}

        for name in islander_names:
            knight_checks[name] = widgets.Checkbox(value=False, description=f"{name} is a Knight")
            knave_checks[name] = widgets.Checkbox(value=False, description=f"{name} is a Knave")
            display(knight_checks[name])
            display(knave_checks[name])

        # Submit button
        submit_button = widgets.Button(description="Submit")
        display(submit_button)

        # Handler for submit button
        def on_submit(b):
            user_knights = [name for name in islander_names if knight_checks[name].value]
            user_knaves = [name for name in islander_names if knave_checks[name].value]

            # Check for conflicting selections
            conflicts = set(user_knights) & set(user_knaves)
            if conflicts:
                print(f"\nConflict: The following names are marked both Knight and Knave: {pretty_print_list(list(conflicts))}")
                return

            # Validate the user's selection
            correct_knights = puzzle.knight_names()
            correct_knaves = puzzle.knave_names()

            # Check if the user's guesses are correct
            if set(user_knights) == set(correct_knights) and set(user_knaves) == set(correct_knaves):
                print("\nCongratulations! Your answers are correct.")
                game_state['puzzles_solved'] += 1
                if game_state['puzzles_solved'] < 3:
                    print(f"You need to solve {3 - game_state['puzzles_solved']} more puzzle(s) at this level.\n")
                    submit_button.on_click(on_submit, remove=True)
                    next_puzzle()
                else:
                    print(f"You have completed the {difficulty} level!\n")
                    game_state['level_index'] += 1
                    game_state['puzzles_solved'] = 0
                    submit_button.on_click(on_submit, remove=True)
                    next_puzzle()
            else:
                print("\nYour answers are incorrect.")
                print(f"The Knights are: {pretty_print_list(correct_knights)}")
                print(f"The Knaves are: {pretty_print_list(correct_knaves)}")
                print("\nLet's try another puzzle at this level.\n")
                submit_button.on_click(on_submit, remove=True)
                next_puzzle()

        submit_button.on_click(on_submit)

    # Start the game
    next_puzzle()

def print_game_solutions():
    difficulties = ['Easy', 'Medium', 'Hard']
    total_puzzles = 9
    puzzles_per_level = total_puzzles // len(difficulties)
    puzzle_number = 1

    for difficulty in difficulties:
        print(f"\n{'=' * 50}")
        print(f"{difficulty} Level Puzzles")
        print(f"{'=' * 50}")
        for _ in range(puzzles_per_level):
            print(f"\nPuzzle {puzzle_number}:\n{'-' * 40}")
            # Generate puzzle
            generator = PuzzleGenerator()
            if difficulty == 'Easy':
                generator.easy()
            elif difficulty == 'Medium':
                generator.medium()
            elif difficulty == 'Hard':
                generator.hard()
            else:
                generator.easy()

            puzzle = generator.puzzle

            # Display the puzzle description
            controller = generator.controller()
            description = controller.accusation_display()
            print(description)

            # Solve the puzzle
            solver = Solver(puzzle)
            reasoning = solver.solve()
            print("\nSolution:")
            print(reasoning)
            print('-' * 40)
            puzzle_number += 1
