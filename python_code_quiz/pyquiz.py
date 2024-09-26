from IPython.display import display
import ipywidgets as widgets
import traceback
import random
import json
import urllib.request
import itertools
import pandas as pd
import contextlib
import io

# Sample input lists (same as before)
int_inputs = [0, 1, -1, 2, -2, 5, -5, 10, -10, 100, -100, -50, 2147483647, -2147483648]  # Including max/min int
float_inputs = [0.0, 1.5, -1.5, 3.14, -3.14, float('inf'), float('-inf'), float('nan')]  # Including infinity and NaN
string_inputs = [
    "",  # Empty string
    "hello",
    "world",
    "Python",
    "AI",
    "The Matrix",
    "HAL 9000",
    "42",
    "Dune",
    "Blade Runner",
    "I, Robot",
    "Ender's Game",
    "Neuromancer",
    "Do Androids Dream of Electric Sheep?",
    "The Hitchhiker's Guide to the Galaxy",
    "2001: A Space Odyssey",
    "Fahrenheit 451",
    "Brave New World",
    "Nineteen Eighty-Four"
]
list_inputs = [
    [],  # Empty list
    [1, 2, 3],
    [-1, -2, -3],
    [0],
    [42],
    [3.14, 2.71],
    ["hello", "world"],
    ["Dune", "Neuromancer", "Foundation"],
    list(range(100)),  # Large list
    [None, True, False],
    [[1, 2], [3, 4]]  # Nested list
]
dict_inputs = [
    {},  # Empty dictionary
    {"a": 1, "b": 2},
    {"key": "value"},
    {"HAL 9000": "I'm sorry Dave, I'm afraid I can't do that."},
    {42: "The Answer"},
    {"nested": {"inner_key": "inner_value"}},
    dict(zip(range(5), string_inputs[:5])),  # Mapping ints to strings
    {"infinite": float('inf'), "nan": float('nan')}
]
bool_inputs = [True, False]
special_inputs = [None, "", [], {}, float('nan'), float('inf'), float('-inf')]

class Question:
    """
    Represents a coding question for the practice tool.
    """
    def __init__(self, function_name, parameters, description, input_type, answer_code, hint='', test_inputs=None):
        """
        Initializes a new Question instance.

        Args:
            function_name (str): The name of the function to implement.
            parameters (list): List of parameter names for the function.
            description (str): Description of what the function should do.
            input_type (str or list): The type(s) of inputs ('int', 'string', 'float', etc.).
            answer_code (str): The code of the correct answer.
            hint (str): A hint to help solve the question.
            test_inputs (list, optional): Predefined test inputs for the question.
        """
        self.function_name = function_name
        self.parameters = parameters
        self.description = description
        self.input_type = input_type
        self.answer_code = answer_code
        self.hint = hint

        # Use predefined test_inputs if provided; otherwise, generate them
        if test_inputs is not None:
            self.test_inputs = test_inputs
            # Draw sample_inputs from test_inputs
            num_samples = 3  # Number of sample inputs to display
            if len(self.test_inputs) <= num_samples:
                self.sample_inputs = self.test_inputs.copy()
            else:
                self.sample_inputs = random.sample(self.test_inputs, num_samples)
        else:
            # Generate sample_inputs and test_inputs as before
            self.sample_inputs = self.generate_inputs(sample=True)
            self.test_inputs = self.generate_inputs(sample=False)

    def generate_inputs(self, sample=True):
        """
        Generates inputs for sample runs or test cases.

        Args:
            sample (bool): If True, generates sample inputs; else, test inputs.

        Returns:
            list: A list of inputs (tuples or single values).
        """
        # Map input types to their respective input lists
        input_type_map = {
            'int': int_inputs,
            'float': float_inputs,
            'string': string_inputs,
            'list': list_inputs,
            'dict': dict_inputs,
            'bool': bool_inputs,
            'special': special_inputs
        }

        # Support multiple input types per question
        if isinstance(self.input_type, str):
            input_types = [self.input_type] * len(self.parameters)
        elif isinstance(self.input_type, list):
            input_types = self.input_type
        else:
            input_types = ['int'] * len(self.parameters)  # Default to 'int'

        # Generate inputs based on input types
        param_inputs = [input_type_map.get(it, []) for it in input_types]

        # Generate all possible combinations of parameter inputs
        all_combinations = list(itertools.product(*param_inputs))

        if sample:
            num_inputs = 3  # Number of sample inputs to display
            # Ensure we have enough combinations to sample from
            if len(all_combinations) <= num_inputs:
                inputs = all_combinations
            else:
                inputs = random.sample(all_combinations, num_inputs)
        else:
            # Limit the number of test cases to 10
            max_tests = 10
            if len(all_combinations) > max_tests:
                inputs = random.sample(all_combinations, max_tests)
            else:
                inputs = all_combinations

        # Flatten the input if there's only one parameter
        inputs = [inp if len(inp) > 1 else inp[0] for inp in inputs]
        return inputs

class PracticeTool:
    """
    A practice tool for coding questions using IPython widgets.
    """
    def __init__(self, questions=None, json_url=None):
        if json_url:
            self.questions = self.load_questions_from_json(json_url)
        else:
            self.questions = questions or []
        self.current_question_index = 0

        # Initialize widgets
        self._create_widgets()
        self._setup_layout()
        self._attach_event_handlers()

        # Display the first question
        self.display_question()
        display(self.tab)

    def _create_widgets(self):
        """Create all widgets used in the UI."""
        self.code_input = widgets.Textarea(
            value='',
            placeholder='Type your code here',
            layout=widgets.Layout(width='100%', height='200px'),
            disabled=False
        )

        self.run_button = widgets.Button(
            description='Run',
            disabled=False,
            button_style='success',
            tooltip='Run your code',
            icon='check',
            layout=widgets.Layout(margin='5px')
        )

        self.retry_button = widgets.Button(
            description='Retry',
            disabled=False,
            button_style='warning',
            tooltip='Clear your code and try again',
            icon='refresh',
            layout=widgets.Layout(margin='5px')
        )

        self.next_button = widgets.Button(
            description='Next',
            disabled=True,  # Initially disabled
            button_style='info',
            tooltip='Go to the next question',
            icon='arrow-right',
            layout=widgets.Layout(margin='5px')
        )

        self.hint_button = widgets.Button(
            description='Show Hint',
            disabled=False,
            button_style='primary',
            tooltip='Show a hint for this question',
            icon='lightbulb-o',
            layout=widgets.Layout(margin='5px')
        )

        # Output areas for test results, hints, and program output
        self.results_area = widgets.Output()
        self.hint_area = widgets.Output()
        self.program_output_area = widgets.Output()

        # Progress bar
        self.progress = widgets.IntProgress(
            value=0,
            min=0,
            max=len(self.questions),
            description='Progress:',
            bar_style='info',
            orientation='horizontal',
            layout=widgets.Layout(width='100%')
        )

        # Create tabs
        self.tab = widgets.Tab()
        self.problem_box = widgets.VBox()
        self.tab.children = [self.problem_box, self.results_area, self.program_output_area]
        self.tab.set_title(0, 'Problem')
        self.tab.set_title(1, 'Test Results')
        self.tab.set_title(2, 'Program Output')

    def _setup_layout(self):
        """Set up the layout of widgets."""
        # Buttons layout
        self.buttons = widgets.HBox([self.run_button, self.retry_button, self.next_button, self.hint_button])

    def _attach_event_handlers(self):
        """Attach event handlers to widgets."""
        self.run_button.on_click(self.execute_student_code)
        self.retry_button.on_click(self.retry_question)
        self.next_button.on_click(self.next_question)
        self.hint_button.on_click(self.show_hint)

    def load_questions_from_json(self, url):
        """
        Loads questions from a JSON URL or file path.

        Args:
            url (str): The URL or file path to load the JSON from.

        Returns:
            list: A list of Question instances.
        """
        try:
            if url.startswith('http'):
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
            else:
                with open(url, 'r') as f:
                    data = json.load(f)
            questions = []
            for item in data['questions']:
                question = Question(
                    function_name=item['function_name'],
                    parameters=item['parameters'],
                    description=item['description'],
                    input_type=item['input_type'],
                    answer_code=item['answer_code'],
                    hint=item.get('hint', ''),
                    test_inputs=item.get('test_inputs')  # Pass test_inputs if available
                )
                questions.append(question)
            return questions
        except Exception as e:
            print(f"Error loading questions from JSON: {e}")
            return []

    def display_question(self):
        """Displays the current question in the UI."""
        if self.current_question_index >= len(self.questions):
            self.problem_box.children = [widgets.HTML("<h3>You've completed all the questions!</h3>")]
            self.next_button.disabled = True
            self.progress.value = len(self.questions)
            return

        # Disable the Next button until the user passes all test cases
        self.next_button.disabled = True

        # Update progress bar
        self.progress.value = self.current_question_index

        question = self.questions[self.current_question_index]
        function_name = question.function_name
        params = ', '.join(question.parameters)

        # Prepopulate code_input with the function signature
        self.code_input.value = f"def {function_name}({params}):\n    pass"

        # Build the question text
        question_text = self.get_question_text(question)
        question_label = widgets.HTML(value=question_text)

        # Clear hint area and program output area
        self.hint_area.clear_output()
        self.program_output_area.clear_output()

        # Update problem box
        self.problem_box.children = [self.progress, question_label, self.code_input, self.buttons, self.hint_area]

        # Clear the results area
        self.results_area.clear_output()
        self.tab.selected_index = 0  # Switch to the Problem tab

    def get_question_text(self, question):
        """Builds the question text including sample runs."""
        function_name = question.function_name
        params = ', '.join(question.parameters)
        description = question.description

        question_text = f"<h3>Question {self.current_question_index + 1} of {len(self.questions)}</h3>"
        question_text += f"<p>Please write a function <b>{function_name}({params})</b> that {description}.</p>"

        # Prepare sample runs
        sample_runs_text = "<h4>Sample Runs:</h4><pre>"
        # Execute the correct function to get sample outputs
        correct_code = question.answer_code
        correct_namespace = {}
        exec(correct_code, correct_namespace)
        correct_func = correct_namespace.get(function_name)

        for sample_input in question.sample_inputs:
            args = sample_input if isinstance(sample_input, tuple) else (sample_input,)
            try:
                result = correct_func(*args)
                args_str = ', '.join(repr(arg) for arg in args)
                sample_runs_text += f"{function_name}({args_str}) ➞ {repr(result)}\n"
            except Exception as e:
                args_str = ', '.join(repr(arg) for arg in args)  # Ensure args_str is defined in exception
                sample_runs_text += f"{function_name}({args_str}) ➞ Error: {e}\n"
        sample_runs_text += "</pre>"

        return question_text + sample_runs_text

    def execute_student_code(self, button):
        """Executes the student's code and displays test results."""
        question = self.questions[self.current_question_index]
        # Clear program output area
        self.program_output_area.clear_output()
        # Clear previous student output
        self.student_output = io.StringIO()
        try:
            student_func = self.run_student_code(question)
            correct_func = self.run_correct_code(question)
            test_results, passed_tests, total_tests = self.run_tests(question, student_func, correct_func)
            self.display_test_results(test_results, passed_tests, total_tests)
            # Display the captured program output
            self.display_program_output(self.student_output.getvalue())
        except Exception:
            with self.results_area:
                self.results_area.clear_output()
                traceback.print_exc()
            self.tab.selected_index = 1  # Switch to Test Results tab

    def run_student_code(self, question):
        """Executes the student's code and returns the student's function."""
        function_name = question.function_name
        student_code = self.code_input.value
        student_namespace = {}
        # Capture any print output during code execution
        with contextlib.redirect_stdout(self.student_output):
            exec(student_code, student_namespace)
        student_func = student_namespace.get(function_name)
        if not student_func:
            raise NameError(f"Function '{function_name}' is not defined.")
        return student_func

    def run_correct_code(self, question):
        """Executes the correct answer code and returns the correct function."""
        function_name = question.function_name
        correct_code = question.answer_code
        correct_namespace = {}
        exec(correct_code, correct_namespace)
        correct_func = correct_namespace.get(function_name)
        return correct_func

    def run_tests(self, question, student_func, correct_func):
        """Runs test cases and returns test results."""
        test_inputs = question.test_inputs
        total_tests = len(test_inputs)
        passed_tests = 0
        test_results = []

        for idx, test_input in enumerate(test_inputs, 1):
            # Determine if test_input is a list or tuple for multiple arguments
            if isinstance(test_input, (list, tuple)):
                args = test_input
            else:
                args = (test_input,)

            try:
                # Capture output during function execution
                with contextlib.redirect_stdout(self.student_output):
                    student_result = student_func(*args)
                correct_result = correct_func(*args)
                args_str = ', '.join(repr(arg) for arg in args)
                passed = student_result == correct_result
                status_icon = '<span style="color: green;">&#10004;</span>' if passed else '<span style="color: red;">&#10008;</span>'
                test_results.append({
                    'Result': status_icon,
                    'Input': f"{question.function_name}({args_str})",
                    'Expected Output': repr(correct_result),
                    'Your Output': repr(student_result)
                })
                if passed:
                    passed_tests += 1
            except Exception as e:
                status_icon = '<span style="color: red;">&#10008;</span>'
                args_str = ', '.join(repr(arg) for arg in args)
                test_results.append({
                    'Result': status_icon,
                    'Input': f"{question.function_name}({args_str})",
                    'Expected Output': 'Error',
                    'Your Output': f"Error: {e}"
                })

        return test_results, passed_tests, total_tests

    def display_test_results(self, test_results, passed_tests, total_tests):
        """Displays the test results in the UI."""
        with self.results_area:
            self.results_area.clear_output()
            df = pd.DataFrame(test_results)
            # Hide the index by resetting it and dropping
            df.reset_index(drop=True, inplace=True)
            # Render the DataFrame as HTML with icons
            df_style = df.style.set_table_styles(
                [{'selector': 'th', 'props': [('text-align', 'left')]}]
            ).set_properties(**{'text-align': 'left'})
            display(widgets.HTML(f"<h3>Test Results: {passed_tests}/{total_tests} Passed</h3>"))
            display(widgets.HTML(df_style.to_html(escape=False, index=False)))
            if passed_tests == total_tests:
                display(widgets.HTML("<b>Congratulations! You passed all test cases! 🎉</b>"))
                self.next_button.disabled = False
            else:
                self.next_button.disabled = True
        # Switch to the Test Results tab
        self.tab.selected_index = 1

    def display_program_output(self, output):
        """Displays the program output in the UI."""
        with self.program_output_area:
            self.program_output_area.clear_output()
            if output.strip():
                display(widgets.HTML(f"<pre>{output}</pre>"))
            else:
                display(widgets.HTML("<i>No output produced.</i>"))

    def retry_question(self, button):
        """Resets the code input and clears test results."""
        question = self.questions[self.current_question_index]
        self.code_input.value = f"def {question.function_name}({', '.join(question.parameters)}):\n    pass"
        self.results_area.clear_output()
        self.hint_area.clear_output()
        self.program_output_area.clear_output()
        self.tab.selected_index = 0  # Switch back to Problem tab
        # Disable the Next button again
        self.next_button.disabled = True

    def next_question(self, button):
        """Advances to the next question."""
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.results_area.clear_output()
            self.hint_area.clear_output()
            self.program_output_area.clear_output()
            self.display_question()
        else:
            # Disable Next button and display completion message
            self.next_button.disabled = True
            self.problem_box.children = [widgets.HTML("<h3>You've completed all the questions!</h3>")]
            self.results_area.clear_output()
            self.program_output_area.clear_output()
            self.tab.selected_index = 0
            self.progress.value = len(self.questions)

    def show_hint(self, button):
        """Displays the hint for the current question."""
        question = self.questions[self.current_question_index]
        with self.hint_area:
            self.hint_area.clear_output()
            if question.hint:
                display(widgets.HTML(f"<b>Hint:</b> {question.hint}"))
            else:
                display(widgets.HTML("<b>Hint:</b> No hint available for this question."))

# Instantiate the practice tool with questions from a JSON file
# practice_tool = PracticeTool(json_url='questions.json')
