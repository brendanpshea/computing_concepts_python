import json
import random
import itertools
import io
import urllib.request
from copy import deepcopy
import contextlib

import numpy as np
import pandas as pd
from IPython.display import display, HTML
import ipywidgets as widgets
import html

# **_INPUT_SAMPLES**: predefined test inputs by type
_INPUT_SAMPLES = {
    'int': [
        0, 1, -1, 2, -2, 5, -5, 10, -10, 100, -100, -50,
        2147483647, 2147483648
    ],
    'float': [
        0.0, 1.5, -1.5, 3.14, -3.14,
        float('inf'), float('-inf'), float('nan')
    ],
    'string': [
        "", "hello", "world", "Python", "AI", "The Matrix", "HAL 9000", "42",
        "Dune", "Blade Runner", "I, Robot", "Ender's Game", "Neuromancer",
        "Do Androids Dream of Electric Sheep?", "The Hitchhiker's Guide to the Galaxy",
        "2001: A Space Odyssey", "Fahrenheit 451", "Brave New World", "Nineteen Eighty-Four"
    ],
    'list': [
        [], [1, 2, 3], [-1, -2, -3], [0], [42], [3.14, 2.71],
        ["hello", "world"], ["Dune", "Neuromancer", "Foundation"], list(range(100)),
        [None, True, False], [[1, 2], [3, 4]]
    ],
    'dict': [
        {}, {"a": 1, "b": 2}, {"key": "value"},
        {"HAL 9000": "I'm sorry Dave, I'm afraid I can't do that."},
        {42: "The Answer"}, {"nested": {"inner_key": "inner_value"}},
        dict(zip(range(5), ["", "hello", "world", "Python", "AI"])),
        {"infinite": float('inf'), "nan": float('nan')}
    ],
    'bool': [True, False],
}
_INPUT_SAMPLES['special'] = [None, "", [], {}, float('nan'), float('inf'), float('-inf')]
_INPUT_SAMPLES['any'] = sum(_INPUT_SAMPLES.values(), [])


def _clone(obj):
    return obj.copy() if isinstance(obj, np.ndarray) else deepcopy(obj)


class Question:
    def __init__(
        self, function_name, parameters, description,
        input_type, answer_code, hint='', test_inputs=None
    ):
        self.function_name = function_name
        self.parameters    = parameters
        self.description   = description
        self.input_type    = input_type
        self.answer_code   = answer_code
        self.hint          = hint
        self.test_inputs   = test_inputs or self.generate_inputs()
        self.sample_inputs = random.sample(self.test_inputs, min(3, len(self.test_inputs)))

    def _param_types(self):
        return (
            [self.input_type] * len(self.parameters)
            if isinstance(self.input_type, str)
            else list(self.input_type)
        )

    def generate_inputs(self, max_tests=10):
        samples = [_INPUT_SAMPLES.get(t, []) for t in self._param_types()]
        combos  = list(itertools.product(*samples))
        chosen  = random.sample(combos, min(max_tests, len(combos)))
        return [args[0] if len(args) == 1 else args for args in chosen]


class PracticeTool:
    def __init__(self, questions=None, json_url=None):
        self.questions      = self._load_questions(json_url) if json_url else questions or []
        self.current_index  = 0
        self.student_output = io.StringIO()
        self._setup_widgets()
        self._show_directions()
        self._show_question()
        display(self.main)

    def _load_questions(self, url):
        try:
            data = (
                json.loads(urllib.request.urlopen(url).read().decode())
                if url.startswith('http')
                else json.load(open(url))
            )
            return [Question(**q) for q in data.get('questions', [])]
        except Exception as e:
            print(f"Error loading questions: {e}")
            return []

    def _setup_widgets(self):
        w = widgets

        # Left panel widgets
        self.progress        = w.IntProgress(min=0, max=len(self.questions),
                                           description='Progress:', layout=w.Layout(width='100%'))
        self.question_output = w.Output()
        self.code_input      = w.Textarea(layout=w.Layout(width='100%', height='200px'))
        self.run_btn         = w.Button(description='Run',    button_style='success', icon='check')
        self.retry_btn       = w.Button(description='Retry',  button_style='warning', icon='refresh')
        self.next_btn        = w.Button(description='Next',   button_style='info',    icon='arrow-right', disabled=True)
        self.hint_btn        = w.Button(description='Show Hint', button_style='primary', icon='lightbulb-o')
        self.skip_dd         = w.Dropdown(options=[], description='Skip to:', layout=w.Layout(width='200px'))
        self.hint_output     = w.Output()

        left_children = [
            self.progress,
            self.question_output,
            self.code_input,
            w.HBox([self.run_btn, self.retry_btn, self.next_btn, self.hint_btn, self.skip_dd]),
            self.hint_output
        ]

        # Right panel widgets
        self.sample_output   = w.Output()
        self.results_output  = w.Output()
        self.program_output  = w.Output()
        self.results_retry   = w.Button(description='Retry', button_style='warning', icon='refresh')
        self.results_next    = w.Button(description='Next',  button_style='info',    icon='arrow-right', disabled=True)

        right_children = [
            widgets.HTML("<h3>Sample Inputs and Outputs</h3>"),
            self.sample_output,
            widgets.HTML("<h3>Results</h3>"),
            self.results_output,
            widgets.HTML("<h3>Output</h3>"),
            self.program_output
        ]

        self.left_panel  = w.VBox(left_children,  layout=w.Layout(width='50%'))
        self.right_panel = w.VBox(right_children, layout=w.Layout(width='50%'))
        self.main        = w.HBox([self.left_panel, self.right_panel], layout=w.Layout(width='100%'))

        # Callbacks
        self.run_btn.on_click(self._run)
        self.retry_btn.on_click(self._reset)
        self.next_btn.on_click(self._next)
        self.hint_btn.on_click(self._hint)
        self.results_retry.on_click(self._reset)
        self.results_next.on_click(self._next)
        self.skip_dd.observe(self._skip, names='value')

    def _show_directions(self):
        with self.question_output:
            self.question_output.clear_output()
            display(HTML("""
<h2>Welcome to the Python Practice Tool</h2>
<p>Practice writing Python functions.</p>
<ul>
  <li>Write your function in the left pane.</li>
  <li>Click <strong>Run</strong> to test.</li>
  <li>Click <strong>Retry</strong> to reset.</li>
  <li>Click <strong>Next</strong> after passing all tests.</li>
  <li>Use <strong>Show Hint</strong> if needed.</li>
</ul>
"""))

    def _show_question(self):
        if self.current_index >= len(self.questions):
            self.left_panel.children = [widgets.HTML("<h3>All questions completed!</h3>")]
            return

        q = self.questions[self.current_index]
        self.progress.value        = self.current_index
        self.next_btn.disabled     = True
        self.results_next.disabled = True

        sig = f"def {q.function_name}({', '.join(q.parameters)}):\n    pass"
        self.code_input.value = sig

        self.skip_dd.options = [(f"Problem {i+1}", i) for i in range(len(self.questions))]
        self.skip_dd.value   = self.current_index

        # render question text
        with self.question_output:
            self.question_output.clear_output()
            display(HTML(f"<h3>Question {self.current_index+1} of {len(self.questions)}</h3><p>{q.description}</p>"))

        # render sample table
        self._render_sample_table(q)

        # clear results/output
        self.results_output.clear_output()
        self.program_output.clear_output()

    def _render_sample_table(self, q):
        func = self._get_func(q.answer_code, q.function_name)
        rows = []
        for inp in q.sample_inputs:
            args = self._prepare_args(inp, clone=True)
            try:
                out = func(*args)
                rows.append((repr(inp), html.escape(repr(out))))
            except Exception as e:
                rows.append((repr(inp), f"Error: {e}"))
        df = pd.DataFrame(rows, columns=['Input', 'Output'])
        with self.sample_output:
            self.sample_output.clear_output()
            display(HTML(df.to_html(index=False, escape=False)))

    def _run(self, _):
        q = self.questions[self.current_index]
        self.program_output.clear_output()
        self.student_output = io.StringIO()

        try:
            student = self._get_func(self.code_input.value, q.function_name)
            correct = self._get_func(q.answer_code,    q.function_name)
            results = self._test(q, student, correct)
        except Exception as e:
            results = [{'Result':'Error','Input':'','Expected':'','Your Output':str(e)}]

        self._show_results(results)
        self._show_program_output()

    def _show_results(self, results):
        total  = len(results)
        passed = sum(1 for r in results if r['Result'] == 'Pass')
        status = "All tests passed!" if passed == total else f"{passed}/{total} tests passed"
        color  = "green" if passed == total else "red"
        self.next_btn.disabled     = (passed != total)
        self.results_next.disabled = (passed != total)

        with self.results_output:
            self.results_output.clear_output()
            display(HTML(f"<h4 style='color:{color}'>{status}</h4>"))
            df = pd.DataFrame(results)
            display(HTML(df.to_html(index=False, escape=False)))
            display(widgets.HBox([self.results_retry, self.results_next]))

    def _show_program_output(self):
        with self.program_output:
            self.program_output.clear_output()
            out = self.student_output.getvalue().strip()
            display(HTML(f"<pre>{out}</pre>") if out else HTML("<i>No output produced.</i>"))

    def _get_func(self, code, name):
        ns = {}
        with contextlib.redirect_stdout(self.student_output):
            exec(code, ns)
        func = ns.get(name)
        if not callable(func):
            raise NameError(f"Function '{name}' not defined")
        return func

    def _compare(self, a, b):
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            return np.array_equal(a, b)
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(self._compare(x, y) for x, y in zip(a, b))
        if isinstance(a, dict) and isinstance(b, dict):
            return a.keys() == b.keys() and all(self._compare(a[k], b[k]) for k in a)
        return a == b

    def _prepare_args(self, inp, clone=False):

        # Handle tuple and set type specifications
        if isinstance(inp, list) and len(inp) == 2 and isinstance(inp[0], str):
            if inp[0] == "tuple":
                inp = tuple(inp[1])
            elif inp[0] == "set":
                inp = set(inp[1])
        
        if isinstance(inp, (list, tuple)):
            return tuple(_clone(x) if clone else x for x in inp)
        val = _clone(inp) if clone else inp
        return (val,)

    def _test(self, q, student, correct):
        results, passed = [], 0
        for inp in q.test_inputs:
            s_args = self._prepare_args(inp, clone=True)
            c_args = self._prepare_args(inp, clone=True)
            try:
                exp = correct(*c_args)
                out = student(*s_args)
                ok  = self._compare(out, exp)
                status = 'Pass' if ok else 'Fail'
                passed += ok
                results.append({
                    'Result':      status,
                    'Input':       repr(inp),
                    'Expected':    repr(exp),
                    'Your Output': repr(out)
                })
            except Exception as e:
                results.append({
                    'Result':      'Error',
                    'Input':       repr(inp),
                    'Expected':    repr(exp),
                    'Your Output': str(e)
                })
        return results

    def _reset(self, _):
        q = self.questions[self.current_index]
        self.code_input.value = f"def {q.function_name}({', '.join(q.parameters)}):\n    pass"
        self.results_output.clear_output()
        self.program_output.clear_output()
        self.hint_output.clear_output()
        self.next_btn.disabled     = True
        self.results_next.disabled = True

    def _next(self, _):
        self.current_index += 1
        self._show_question()

    def _hint(self, _):
        q = self.questions[self.current_index]
        with self.hint_output:
            self.hint_output.clear_output()
            display(HTML(f"<b>Hint:</b> {q.hint or 'No hint available.'}"))

    def _skip(self, change):
        idx = change['new']
        if idx != self.current_index:
            self.current_index = idx
            self._show_question()
