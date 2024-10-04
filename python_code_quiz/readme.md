# PyQuiz: Interactive Python Coding Practice Tool

PyQuiz is an interactive Python coding practice tool designed to help students learn and practice Python programming through a series of coding questions. It provides a user-friendly interface using IPython widgets, making it ideal for use in Jupyter notebooks or similar interactive Python environments.

## Features

- Interactive coding questions with real-time feedback
- Support for multiple question types and input formats
- Customizable questions loaded from JSON files
- Hint system for additional guidance
- Progress tracking
- Test case execution and result display
- Program output capture and display

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:

   ```
   pip install ipywidgets pandas numpy
   ```

3. Download the `pyquiz.py` file from the GitHub repository:

   ```
   wget https://github.com/brendanpshea/computing_concepts_python/raw/main/python_code_quiz/pyquiz.py
   ```

## Usage

1. In your Jupyter notebook or interactive Python environment, import the `PracticeTool` class:

   ```python
   from pyquiz import PracticeTool
   ```

2. Create an instance of the `PracticeTool` class, specifying the path to your JSON file containing the questions:

   ```python
   practice_tool = PracticeTool(json_url='path_to_your_questions.json')
   ```

   You can also use a URL to load questions from a remote source:

   ```python
   practice_tool = PracticeTool(json_url='https://example.com/questions.json')
   ```

3. The tool will automatically display and allow interaction with the coding questions.

## Creating Custom Questions

To create your own set of questions, prepare a JSON file in the following format:

```json
{
  "questions": [
    {
      "function_name": "example_function",
      "parameters": ["param1", "param2"],
      "description": "Write a function that does X",
      "input_type": ["int", "string"],
      "answer_code": "def example_function(param1, param2):\n    # Correct implementation here\n    return result",
      "hint": "Consider using method Y",
      "test_inputs": [[1, "a"], [2, "b"]]
    },
    // Add more questions here
  ]
}
```

- `function_name`: The name of the function to be implemented
- `parameters`: List of parameter names for the function
- `description`: A description of what the function should do
- `input_type`: Types of inputs for each parameter (can be a single string for all parameters)
- `answer_code`: The correct implementation of the function
- `hint` (optional): A hint to help students if they get stuck
- `test_inputs` (optional): Custom test inputs for the function

## Features in Detail

### Question Display
- Questions are presented one at a time with a clear description and function signature.
- Sample runs are displayed to help students understand the expected behavior.

### Code Input
- Students can write their code in a text area with syntax highlighting.
- The initial function signature is provided automatically.

### Test Execution
- Students can run their code against predefined test cases.
- Test results are displayed in a color-coded table for easy interpretation.

### Hint System
- Each question can have an optional hint that students can reveal if needed.

### Progress Tracking
- A progress bar shows the current question number and total questions.
- Students can skip to specific questions using a dropdown menu.

### Program Output
- Any output produced by the student's code is captured and displayed separately.

## Contributing

Contributions to improve PyQuiz are welcome. Please feel free to submit pull requests or open issues on the GitHub repository.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

- Thanks to all contributors and users who help improve this educational tool.
