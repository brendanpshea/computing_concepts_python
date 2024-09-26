from IPython.display import display, HTML
import ipywidgets as widgets
import traceback
import random
import json
import urllib.request
import itertools
import pandas as pd
import contextlib
import io
import html
import numpy as np

# Sample input lists
int_inputs = [0, 1, -1, 2, -2, 5, -5, 10, -10, 100, -100, -50, 2147483647, -2147483648]
float_inputs = [0.0, 1.5, -1.5, 3.14, -3.14, float('inf'), float('-inf'), float('nan')]
string_inputs = [
    "",
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
    [],
    [1, 2, 3],
    [-1, -2, -3],
    [0],
    [42],
    [3.14, 2.71],
    ["hello", "world"],
    ["Dune", "Neuromancer", "Foundation"],
    list(range(100)),
    [None, True, False],
    [[1, 2], [3, 4]]
]
dict_inputs = [
    {},
    {"a": 1, "b": 2},
    {"key": "value"},
    {"HAL 9000": "I'm sorry Dave, I'm afraid I can't do that."},
    {42: "The Answer"},
    {"nested": {"inner_key": "inner_value"}},
    dict(zip(range(5), string_inputs[:5])),
    {"infinite": float('inf'), "nan": float('nan')}
]
bool_inputs = [True, False]
special_inputs = [None, "", [], {}, float('nan'), float('inf'), float('-inf')]

# Update input_type_map to include 'any'
input_type_map = {
    'int': int_inputs,
    'float': float_inputs,
    'string': string_inputs,
    'list': list_inputs,
    'dict': dict_inputs,
    'bool': bool_inputs,
    'special': special_inputs,
    'any': int_inputs + float_inputs + string_inputs + list_inputs + dict_inputs + bool_inputs + special_inputs
}

class Question:
    """
    Represents a coding question for the practice tool.
    """
    def __init__(self, function_name, parameters, description, input_type, answer_code, hint='', test_inputs=None):
        self.function_name = function_name
        self.parameters = parameters
        self.description = description
        self.input_type = input_type
        self.answer_code = answer_code
        self.hint = hint

        # Initialize test inputs and sample inputs
        self.test_inputs = test_inputs or self.generate_inputs(sample=False)
        self.sample_inputs = random.sample(self.test_inputs, min(3, len(self.test_inputs)))

    def generate_inputs(self, sample=True):
        """
        Generates inputs for sample runs or test cases.
        """
        # Support multiple input types per parameter
        if isinstance(self.input_type, str):
            input_types = [self.input_type] * len(self.parameters)
        elif isinstance(self.input_type, list):
            input_types = self.input_type
        else:
            input_types = ['int'] * len(self.parameters)

        # Generate inputs based on input types
        param_inputs = [input_type_map.get(it, []) for it in input_types]

        # Generate all possible combinations of parameter inputs
        all_combinations = list(itertools.product(*param_inputs))

        # Limit the number of test cases
        max_tests = 10
        inputs = random.sample(all_combinations, min(max_tests, len(all_combinations)))

        # Flatten if only one parameter
        inputs = [inp if len(inp) > 1 else inp[0] for inp in inputs]
        return inputs

class PracticeTool:
    """
    A practice tool for coding questions using IPython widgets.
    """
    def __init__(self, questions=None, json_url=None):
        self.questions = self.load_questions(json_url) if json_url else questions or []
        self.current_question_index = 0
        self.student_output = None

        # Initialize widgets and display the tool
        self.initialize_widgets()
        self.display_directions()
        self.display_question()
        display(self.tab_widget)

    def load_questions(self, url):
        """
        Loads questions from a JSON URL or file path.
        """
        try:
            if url.startswith('http'):
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
            else:
                with open(url, 'r') as file:
                    data = json.load(file)

            questions = [
                Question(
                    function_name=item['function_name'],
                    parameters=item['parameters'],
                    description=item['description'],
                    input_type=item['input_type'],
                    answer_code=item['answer_code'],
                    hint=item.get('hint', ''),
                    test_inputs=item.get('test_inputs')
                )
                for item in data['questions']
            ]
            return questions
        except Exception as e:
            print(f"Error loading questions: {e}")
            return []

    def initialize_widgets(self):
        """Initializes all the widgets used in the UI."""
        # Code input area
        self.code_input = widgets.Textarea(
            value='',
            placeholder='Type your code here',
            layout=widgets.Layout(width='100%', height='200px')
        )

        # Control buttons
        self.run_button = widgets.Button(
            description='Run',
            button_style='success',
            tooltip='Run your code',
            icon='check'
        )
        self.retry_button = widgets.Button(
            description='Retry',
            button_style='warning',
            tooltip='Reset your code',
            icon='refresh'
        )
        self.next_button = widgets.Button(
            description='Next',
            button_style='info',
            tooltip='Next question',
            icon='arrow-right',
            disabled=True
        )
        self.hint_button = widgets.Button(
            description='Show Hint',
            button_style='primary',
            tooltip='Show a hint',
            icon='lightbulb-o'
        )

        # Skip to question dropdown
        self.skip_dropdown = widgets.Dropdown(
            options=[(f"Problem {i+1}", i) for i in range(len(self.questions))],
            description='Skip to:',
            layout=widgets.Layout(width='200px')
        )

        # Output areas
        self.results_output = widgets.Output()
        self.hint_output = widgets.Output()
        self.program_output = widgets.Output()
        self.directions_output = widgets.Output()

        # Progress bar
        self.progress_bar = widgets.IntProgress(
            value=0,
            min=0,
            max=len(self.questions),
            description='Progress:',
            bar_style='info',
            layout=widgets.Layout(width='100%')
        )

        # Tabs
        self.problem_area = widgets.VBox()
        self.tab_widget = widgets.Tab(children=[
            self.directions_output,
            self.problem_area,
            self.results_output,
            self.program_output
        ])
        self.tab_widget.set_title(0, 'Directions')
        self.tab_widget.set_title(1, 'Problem')
        self.tab_widget.set_title(2, 'Test Results')
        self.tab_widget.set_title(3, 'Program Output')

        # Attach event handlers
        self.run_button.on_click(self.run_code)
        self.retry_button.on_click(self.reset_code)
        self.next_button.on_click(self.next_question)
        self.hint_button.on_click(self.show_hint)
        self.skip_dropdown.observe(self.skip_to_question, names='value')

    def display_directions(self):
        """Displays the directions in the Directions tab."""
        with self.directions_output:
            self.directions_output.clear_output()
            directions = """
<h2>Welcome to the Python Practice Tool</h2>
<p>This tool allows you to practice writing Python functions.</p>
<p><strong>Instructions:</strong></p>
<ul>
<li>Read the problem description in the <strong>Problem</strong> tab.</li>
<li>Write your function in the code area provided.</li>
<li>Click <strong>Run</strong> to test your code.</li>
<li>Click <strong>Retry</strong> to reset your code.</li>
<li>Click <strong>Next</strong> to proceed after passing all tests.</li>
<li>Use <strong>Show Hint</strong> if you need assistance.</li>
<li>Select a problem from <strong>Skip to</strong> to navigate directly.</li>
</ul>
<p><strong>Python Function Basics:</strong></p>
<ul>
<li>Define functions using <code>def</code>.</li>
<li>Specify parameters in parentheses.</li>
<li>Indent the function body.</li>
<li>Use <code>return</code> to output a value.</li>
</ul>
"""
            display(widgets.HTML(directions))

    def display_question(self):
        """Displays the current question."""
        if self.current_question_index >= len(self.questions):
            self.problem_area.children = [widgets.HTML("<h3>All questions completed!</h3>")]
            self.next_button.disabled = True
            self.progress_bar.value = len(self.questions)
            return

        # Update progress and disable Next button
        self.progress_bar.value = self.current_question_index
        self.next_button.disabled = True

        question = self.questions[self.current_question_index]
        function_signature = f"def {question.function_name}({', '.join(question.parameters)}):\n    pass"
        self.code_input.value = function_signature

        # Build the question text
        question_text = self.build_question_text(question)
        question_label = widgets.HTML(value=question_text)

        # Clear outputs
        self.hint_output.clear_output()
        self.program_output.clear_output()
        self.results_output.clear_output()
        self.tab_widget.selected_index = 1  # Switch to Problem tab

        # Update problem area
        control_buttons = widgets.HBox([
            self.run_button, self.retry_button, self.next_button,
            self.hint_button, self.skip_dropdown
        ])
        self.problem_area.children = [
            self.progress_bar, question_label, self.code_input,
            control_buttons, self.hint_output
        ]

        # Update skip dropdown
        self.skip_dropdown.value = self.current_question_index

    def build_question_text(self, question):
        """Constructs the question text with sample runs."""
        header = f"<h3>Question {self.current_question_index + 1} of {len(self.questions)}</h3>"
        description = f"<p>Write a function <b>{question.function_name}({', '.join(question.parameters)})</b> to: {question.description}.</p>"
        samples = "<h4>Sample Runs:</h4>"

        # Prepare sample runs using the correct answer code
        correct_func = self.get_function_from_code(question.answer_code, question.function_name)
        sample_data = []
        for sample_input in question.sample_inputs:
            args = self.prepare_arguments(sample_input, question)
            args_str = ', '.join(repr(arg) for arg in args)
            try:
                result = correct_func(*args)
                sample_data.append({
                    'Input': f"{question.function_name}({args_str})",
                    'Output': html.escape(repr(result))
                })
            except Exception as e:
                sample_data.append({
                    'Input': f"{question.function_name}({args_str})",
                    'Output': f"Error: {html.escape(str(e))}"
                })

        # Create a pandas DataFrame and style it
        df = pd.DataFrame(sample_data)
        styled_df = df.style.set_properties(**{
            'text-align': 'left',
            'white-space': 'pre-wrap',
            'border': '1px solid black',
            'padding': '8px'
        })
        styled_df = styled_df.set_table_styles([
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left'), ('border', '1px solid black'), ('padding', '8px')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('border', '1px solid black'), ('padding', '8px')]},
            {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
        ])

        # Convert the styled DataFrame to HTML and wrap it in a div for proper rendering
        samples += f'<div style="overflow-x: auto;">{styled_df.to_html(escape=False)}</div>'

        return header + description + samples

    def run_code(self, _):
        """Executes the student's code and displays test results."""
        question = self.questions[self.current_question_index]
        self.program_output.clear_output()
        self.student_output = io.StringIO()

        try:
            student_func = self.get_function_from_code(self.code_input.value, question.function_name)
            correct_func = self.get_function_from_code(question.answer_code, question.function_name)
            test_results = self.execute_tests(question, student_func, correct_func)
            self.display_test_results(test_results)
            self.display_program_output()
        except Exception:
            with self.results_output:
                self.results_output.clear_output()
                traceback.print_exc()
            self.tab_widget.selected_index = 2  # Switch to Test Results tab

    def get_function_from_code(self, code, function_name):
        """Compiles code and retrieves the specified function."""
        namespace = {}
        with contextlib.redirect_stdout(self.student_output):
            exec(code, namespace)
        func = namespace.get(function_name)
        if not func:
            raise NameError(f"Function '{function_name}' is not defined.")
        return func

    def object_compare(self, obj1, obj2):
        """
        Compare two arbitrary Python objects, including NumPy arrays.
        """
        if isinstance(obj1, np.ndarray) and isinstance(obj2, np.ndarray):
            return np.array_equal(obj1, obj2)
        elif isinstance(obj1, (list, tuple)) and isinstance(obj2, (list, tuple)):
            return len(obj1) == len(obj2) and all(self.object_compare(e1, e2) for e1, e2 in zip(obj1, obj2))
        elif isinstance(obj1, dict) and isinstance(obj2, dict):
            return obj1.keys() == obj2.keys() and all(self.object_compare(obj1[k], obj2[k]) for k in obj1.keys())
        else:
            return obj1 == obj2

    def execute_tests(self, question, student_func, correct_func):
        """Executes test cases and collects results."""
        test_results = []
        total_tests = len(question.test_inputs)
        passed_tests = 0

        for test_input in question.test_inputs:
            args = self.prepare_arguments(test_input, question)
            args_str = ', '.join(repr(arg) for arg in args)

            try:
                with contextlib.redirect_stdout(self.student_output):
                    student_output = student_func(*args)
                correct_output = correct_func(*args)
                passed = self.object_compare(student_output, correct_output)
                status = 'Pass' if passed else 'Fail'
                test_results.append({
                    'Result': status,
                    'Input': f"{question.function_name}({args_str})",
                    'Expected Output': repr(correct_output),
                    'Your Output': repr(student_output)
                })
                if passed:
                    passed_tests += 1
            except Exception as e:
                test_results.append({
                    'Result': 'Error',
                    'Input': f"{question.function_name}({args_str})",
                    'Expected Output': repr(correct_output),
                    'Your Output': f"Error: {str(e)}"
                })

        # Update Next button status
        self.next_button.disabled = passed_tests < total_tests
        return test_results

    def display_test_results(self, test_results):
        """Displays the test results in the UI."""
        with self.results_output:
            self.results_output.clear_output()
            df = pd.DataFrame(test_results)

            # Define a function to apply color coding
            def color_result(val):
                if val == 'Pass':
                    return 'background-color: #90EE90'  # Light green
                elif val == 'Fail':
                    return 'background-color: #FFCCCB'  # Light red
                elif val == 'Error':
                    return 'background-color: #FFD700'  # Gold
                return ''

            # Apply the color coding and other styles
            styled_df = df.style.map(color_result, subset=['Result'])
            styled_df = styled_df.set_properties(**{
                'text-align': 'left',
                'white-space': 'pre-wrap',
                'border': '1px solid black',
                'padding': '8px'
            })
            styled_df = styled_df.set_table_styles([
                {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left'), ('border', '1px solid black'), ('padding', '8px')]},
                {'selector': 'td', 'props': [('text-align', 'left'), ('border', '1px solid black'), ('padding', '8px')]},
                {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
            ])

            # Convert the styled DataFrame to HTML and wrap it in a div for proper rendering
            html_table = f'<div style="overflow-x: auto;">{styled_df.to_html(escape=False)}</div>'
            display(HTML(html_table))

            if not self.next_button.disabled:
                display(widgets.HTML("<b>All test cases passed! Click Next to continue.</b>"))
        self.tab_widget.selected_index = 2  # Switch to Test Results tab

    def display_program_output(self):
        """Displays any output produced during code execution."""
        output = self.student_output.getvalue()
        with self.program_output:
            self.program_output.clear_output()
            if output.strip():
                display(widgets.HTML(f"<pre>{output}</pre>"))
            else:
                display(widgets.HTML("<i>No output produced.</i>"))

    def prepare_arguments(self, test_input, question):
        """Prepares arguments for function calls."""
        num_params = len(question.parameters)
        if num_params == 1:
            return (test_input,)
        elif isinstance(test_input, (list, tuple)) and len(test_input) == num_params:
            return tuple(test_input)
        else:
            raise ValueError(f"Invalid test input: {test_input}")

    def reset_code(self, _):
        """Resets the code input and clears outputs."""
        question = self.questions[self.current_question_index]
        self.code_input.value = f"def {question.function_name}({', '.join(question.parameters)}):\n    pass"
        self.results_output.clear_output()
        self.hint_output.clear_output()
        self.program_output.clear_output()
        self.tab_widget.selected_index = 1  # Switch to Problem tab
        self.next_button.disabled = True

    def next_question(self, _):
        """Advances to the next question."""
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.problem_area.children = [widgets.HTML("<h3>All questions completed!</h3>")]
            self.next_button.disabled = True
            self.progress_bar.value = len(self.questions)
            self.results_output.clear_output()
            self.program_output.clear_output()
            self.tab_widget.selected_index = 1

    def show_hint(self, _):
        """Displays the hint for the current question."""
        question = self.questions[self.current_question_index]
        with self.hint_output:
            self.hint_output.clear_output()
            hint_text = f"<b>Hint:</b> {question.hint}" if question.hint else "<b>No hint available.</b>"
            display(widgets.HTML(hint_text))

    def skip_to_question(self, change):
        """Handles the skip to question event."""
        new_index = change['new']
        if new_index != self.current_question_index:
            self.current_question_index = new_index
            self.display_question()

# Instantiate the practice tool with questions from a JSON file
# practice_tool = PracticeTool(json_url='questions2.json')
