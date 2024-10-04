# Loop of the Recursive Dragon

Loop of the Recursive Dragon is an interactive quiz game designed to make learning fun and engaging. It combines elements of role-playing games with educational quizzes, allowing users to battle monsters by answering questions correctly.

## Features

- Interactive quiz gameplay
- RPG elements including monsters, weapons, and armor
- Customizable questions and monsters
- Runs in Jupyter notebooks, including Google Colab

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook or Google Colab
- Required Python libraries: `json`, `random`, `dataclasses`, `typing`, `ipywidgets`, `IPython`

### Installation

1. If you're using Google Colab, you can directly download the script using:

   ```
   !wget https://github.com/brendanpshea/computing_concepts_python/raw/main/lotr/lotr.py
   ```

2. If you're using a local Jupyter notebook, download the `lotr.py` file and place it in your working directory.

### Usage

1. Import the game:

   ```python
   from lotr import start_game
   ```

2. Start the game by calling the `start_game` function with the path to your questions JSON file:

   ```python
   start_game("path_to_your_questions.json")
   ```

   You can also specify a custom monsters file:

   ```python
   start_game("path_to_your_questions.json", "path_to_your_monsters.json")
   ```

   If you don't specify a monsters file, it will use the default one from the GitHub repository.

3. The game will start, and you can interact with it using the provided buttons and checkboxes.

## Creating Custom Questions

To create your own set of questions, prepare a JSON file in the following format:

```json
[
  {
    "question": "What is the capital of France?",
    "correct": ["Paris"],
    "incorrect": ["London", "Berlin", "Madrid"],
    "hint": "This city is known as the City of Light."
  },
  {
    "question": "Which of the following are prime numbers?",
    "correct": ["2", "3", "5", "7"],
    "incorrect": ["1", "4", "6", "8", "9"],
    "hint": "A prime number is only divisible by 1 and itself."
  }
]
```

## Creating Custom Monsters

To create your own set of monsters, prepare a JSON file in the following format:

```json
[
  {
    "monster_name": "Goblin",
    "initial_description": "A small, grotesque creature with sharp teeth.",
    "hit_dice": 2,
    "attack_die": 4,
    "defense": 1
  },
  {
    "monster_name": "Dragon",
    "initial_description": "A massive, fire-breathing beast with scales as hard as steel.",
    "hit_dice": 8,
    "attack_die": 12,
    "defense": 5
  }
]
```

## Contributing

Contributions to improve the game or expand the question/monster database are welcome. Please feel free to submit pull requests or open issues on the GitHub repository.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

- Thanks to all contributors and users who help improve this educational game.
