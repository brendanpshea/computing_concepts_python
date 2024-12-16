# lotr.py

import json
import random
import os
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import ipywidgets as widgets
from IPython.display import display, HTML

# **Utility Functions**
# **load_json(file_path_or_url)**: Loads JSON data and returns an empty list on failure.
def load_json(file_path_or_url: str) -> List[Dict]:
    if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
        try:
            response = requests.get(file_path_or_url)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, json.JSONDecodeError):
            print(f"Error: Could not load or parse JSON from '{file_path_or_url}'.")
            return []
    elif os.path.isfile(file_path_or_url):
        try:
            with open(file_path_or_url, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: Could not load or parse JSON from '{file_path_or_url}'.")
            return []
    else:
        print(f"Error: '{file_path_or_url}' is neither a valid file nor a URL.")
        return []

# **Data**
# Weapons progress from debugging tools to legendary artifacts
WEAPONS = [
    {"name": "Apprentice's Debug Dagger", "attack_die": 4},
    {"name": "Journeyman's Binary Blade", "attack_die": 5},
    {"name": "Recursive Battle Axe", "attack_die": 6},
    {"name": "Greater Sword of Stack Overflow", "attack_die": 7},
    {"name": "Epic Quantum Warhammer", "attack_die": 8},
    {"name": "Ancient Blade of Deep Learning", "attack_die": 9},
    {"name": "Legendary Sword of System Core Access", "attack_die": 10},
]

# Armor progresses from basic protection to legendary defenses
ARMORS = [
    {"name": "Initiate's Firewall Robes", "defense": 0},
    {"name": "Acolyte's Cache Armor", "defense": 1},
    {"name": "Encryption Mesh Vest", "defense": 2},
    {"name": "Greater Blockchain Chainmail", "defense": 3},
    {"name": "Epic Neural Network Plate", "defense": 4},
    {"name": "Ancient Quantum-Shielded Armor", "defense": 5},
    {"name": "Legendary Armor of Root Access", "defense": 6},
]

BBS_CSS = """
<style>
.bbs-container {
    background-color: #1e1e1e;
    border: 2px solid #00ff00;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    color: #00ff00;
    font-family: 'Courier New', Courier, monospace;
}
.title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}
.section {
    font-size: 16px;
    margin-bottom: 10px;
}
.bold { font-weight: bold; }
.underline { text-decoration: underline; }
.yellow { color: #ffff00; }
.red { color: #ff0000; }
.cyan { color: #00ffff; }
</style>
"""

# **Model Classes**: These contain the logic and data of the game, independent of UI.

@dataclass
class Player:
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 50
    max_hit_points: int = 20
    hit_points: int = 20
    weapon: Dict[str, Union[str, int]] = field(default_factory=lambda: WEAPONS[0])
    armor: Dict[str, Union[str, int]] = field(default_factory=lambda: ARMORS[0])
    total_correct: int = 0
    total_incorrect: int = 0

@dataclass
class Monster:
    monster_name: str
    initial_description: str
    hit_dice: int
    attack_die: int
    defense: int
    hit_points: int = field(init=False)
    xp_value: int = field(init=False)

    def __post_init__(self):
        self.hit_points = sum(random.randint(1, 6) for _ in range(self.hit_dice))
        self.xp_value = self.hit_dice * 10

class GameModel:
    def __init__(self, questions_data: List[Dict], monsters_data: List[Dict]):
        self.questions = questions_data[:]
        random.shuffle(self.questions)
        self.questions_to_ask = self.questions.copy()
        self.monsters_data = monsters_data
        self.player = Player()
        self.current_monster: Optional[Monster] = None
        self.current_question: Optional[Dict] = None
        self.questions_asked = 0

    def generate_monster(self) -> Optional[Monster]:
        if not self.monsters_data:
            return None
        valid_monsters = [m for m in self.monsters_data if abs(m['hit_dice'] - self.player.level) <= 1]
        if not valid_monsters:
            valid_monsters = self.monsters_data
        data = random.choice(valid_monsters)
        return Monster(
            monster_name=data["monster_name"],
            initial_description=data.get("initial_description", ""),
            hit_dice=data["hit_dice"],
            attack_die=data["attack_die"],
            defense=data["defense"]
        )

    def next_encounter(self):
        # If no current monster or it's defeated, get a new one
        if not self.current_monster or self.current_monster.hit_points <= 0:
            if not self.questions_to_ask:
                self.current_monster = None
                self.current_question = None
                return "victory"
            self.current_monster = self.generate_monster()

        if self.questions_to_ask:
            self.current_question = self.questions_to_ask.pop(0)
        else:
            self.current_question = None
            return "no_questions"
        return "continue"

    def evaluate_answer(self, selected_options: List[str]) -> Dict[str, Union[int, bool, str]]:
        correct_set = set(self.current_question.get('correct', []))
        incorrect_set = set(self.current_question.get('incorrect', []))
        selected_set = set(selected_options)

        correct_selections = selected_set & correct_set
        incorrect_selections = selected_set & incorrect_set
        missed_correct = correct_set - selected_set

        self.player.total_correct += len(correct_selections)
        self.player.total_incorrect += len(incorrect_selections)

        player_hits = len(correct_selections) + len(incorrect_set - selected_set)
        monster_hits = len(incorrect_selections) + len(missed_correct)

        player_damage = sum(random.randint(1, self.player.weapon['attack_die']) for _ in range(player_hits))
        monster_damage = sum(random.randint(1, self.current_monster.attack_die) for _ in range(monster_hits))

        effective_player_damage = max(player_damage - self.current_monster.defense, 0)
        effective_monster_damage = max(monster_damage - self.player.armor['defense'], 0)

        self.current_monster.hit_points -= effective_player_damage
        self.player.hit_points -= effective_monster_damage

        defeated_monster = False
        defeated_player = False
        xp_gained = 0
        question_repeated = False

        if self.current_monster.hit_points <= 0:
            defeated_monster = True
            xp_gained = self.current_monster.xp_value
            self.player.xp += xp_gained
            self.check_level_up()

        if self.player.hit_points <= 0:
            defeated_player = True

        if missed_correct or incorrect_selections:
            # Re-queue question
            self.questions_to_ask.append(self.current_question)
            question_repeated = True

        self.questions_asked += 1

        return {
            "effective_player_damage": effective_player_damage,
            "effective_monster_damage": effective_monster_damage,
            "defeated_monster": defeated_monster,
            "defeated_player": defeated_player,
            "xp_gained": xp_gained,
            "question_repeated": question_repeated
        }

    def check_level_up(self):
        if self.player.xp >= self.player.xp_to_next_level:
            self.player.level += 1
            self.player.xp_to_next_level += 50
            self.player.max_hit_points += 10
            self.player.hit_points = self.player.max_hit_points
            # Upgrade gear if possible
            if self.player.level <= len(WEAPONS):
                self.player.weapon = WEAPONS[self.player.level - 1]
            if self.player.level <= len(ARMORS):
                self.player.armor = ARMORS[self.player.level - 1]

# **UI Class**: Handles all display and input elements.
class GameUI:
    def __init__(self):
        self.main_container = widgets.VBox(
            layout=widgets.Layout(
                width='800px',
                padding='20px',
                border='solid 1px #00ff00',
                border_radius='10px',
                background_color='black',
                color='green'
            )
        )
        display(HTML(BBS_CSS))
        display(self.main_container)

    def show_initial_screen(self, start_callback):
        initial_html = """
        <div class='bbs-container'>
            <div class='title'>Welcome to the Loop of the Recursive Dragon!</div>
            <div class='section'>
                Face monsters near your level. Answer questions to deal damage and gain XP. Level up to improve gear and health.
            </div>
        </div>
        """
        start_button = widgets.Button(
            description="Start Adventure",
            button_style='success',
            layout=widgets.Layout(width='200px', height='40px')
        )
        start_button.on_click(lambda b: start_callback())
        self.main_container.children = [widgets.HTML(value=initial_html), start_button]

    def show_encounter(self, player: Player, monster: Monster, question: Dict, submit_callback, hint_callback):
        encounter_html = f"""
        <div class='bbs-container'>
            <div class='title'>Loop of the Recursive Dragon</div>
            <div class='section'>
                You encounter <span class='bold underline'>{monster.monster_name}</span>! {monster.initial_description}<br>
                Monster HP: <span class='yellow'>{monster.hit_points}</span><br>
                Your HP: <span class='yellow'>{player.hit_points}/{player.max_hit_points}</span>, Lvl: <span class='yellow'>{player.level}</span>, XP: <span class='yellow'>{player.xp}/{player.xp_to_next_level}</span><br>
                Weapon: <span class='yellow'>{player.weapon['name']}</span>, Armor: <span class='yellow'>{player.armor['name']}</span>
            </div>
        </div>
        <div class='bbs-container'>
            <div class='section'>
                <span class='bold'>Question:</span> {question['question']}
            </div>
        </div>
        """

        # Build answer options
        options = question.get('correct', []) + question.get('incorrect', [])
        random.shuffle(options)
        checkboxes = [widgets.Checkbox(value=False, description=opt, indent=False,
                                       style={'description_width': 'initial'},
                                       layout=widgets.Layout(width='100%'))
                      for opt in options]

        submit_button = widgets.Button(description="Submit Answer", button_style='success')
        hint_button = widgets.Button(description="Show Hint", button_style='info')

        def on_submit(b):
            selected = [cb.description for cb in checkboxes if cb.value]
            submit_callback(selected)

        def on_hint(b):
            h = question.get('hint', 'No hint available.')
            self.show_hint(h)

        submit_button.on_click(on_submit)
        hint_button.on_click(on_hint)

        self.main_container.children = [
            widgets.HTML(value=encounter_html),
            widgets.VBox(checkboxes, layout=widgets.Layout(overflow_y='auto', max_height='300px', width='100%')),
            widgets.HBox([submit_button, hint_button], layout=widgets.Layout(justify_content='center', gap='10px', width='100%'))
        ]

    def show_hint(self, hint: str):
        hint_html = f"<div class='bbs-container'><div class='section'><span class='cyan'>Hint: {hint}</span></div></div>"
        children = list(self.main_container.children)
        # Remove old hint if exists
        children = [ch for ch in children if not (isinstance(ch, widgets.HTML) and 'Hint:' in ch.value)]
        children.append(widgets.HTML(value=hint_html))
        self.main_container.children = tuple(children)

    def show_results(self, player: Player, monster: Optional[Monster], battle_data: Dict, continue_callback):
        battle_results = "<div class='bbs-container'><div class='section'>"
        if battle_data["effective_player_damage"] > 0:
            battle_results += f"You deal <span class='yellow'>{battle_data['effective_player_damage']}</span> damage.<br>"
        else:
            battle_results += "Your attack was ineffective.<br>"

        if battle_data["effective_monster_damage"] > 0:
            battle_results += f"The monster hits you for <span class='red'>{battle_data['effective_monster_damage']}</span> damage.<br>"
        else:
            if (battle_data["defeated_monster"] is False) and (battle_data["effective_monster_damage"] == 0):
                battle_results += "The monster cannot penetrate your armor.<br>"
            else:
                battle_results += "No counter-attack from the monster.<br>"

        if battle_data["defeated_monster"]:
            battle_results += f"<span class='bold'>You defeated the monster!</span><br>"
            battle_results += f"XP gained: <span class='yellow'>{battle_data['xp_gained']}</span> (Total: {player.xp}/{player.xp_to_next_level})<br>"

        if battle_data["defeated_player"]:
            battle_results += f"<span class='red bold'>You have been defeated! Game Over.</span></div></div>"
            self.main_container.children = [widgets.HTML(value=battle_results)]
            return

        if monster and monster.hit_points > 0:
            battle_results += f"Monster HP: <span class='yellow'>{monster.hit_points}</span><br>"

        battle_results += f"Your HP: <span class='yellow'>{player.hit_points}/{player.max_hit_points}</span><br>"
        if battle_data["question_repeated"]:
            battle_results += "<span class='cyan'>You will face this question again.</span><br>"
        battle_results += "</div></div>"

        continue_button = widgets.Button(description="Continue", button_style='primary', layout=widgets.Layout(width='150px'))
        continue_button.on_click(lambda b: continue_callback())
        self.main_container.children = [widgets.HTML(value=battle_results), continue_button]

    def show_no_questions(self, player: Player):
        no_q_html = f"""
        <div class='bbs-container'>
            <div class='section'>
                <span class='bold red'>All questions have been answered!</span> The monster flees.
            </div>
            <div class='section'>
                <span class='bold'>Final Stats:</span><br>
                Correct: <span class='yellow'>{player.total_correct}</span><br>
                Incorrect: <span class='yellow'>{player.total_incorrect}</span><br>
                HP: <span class='yellow'>{player.hit_points}/{player.max_hit_points}</span><br>
                Level: <span class='yellow'>{player.level}</span>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=no_q_html)]

    def show_victory(self, player: Player):
        victory_html = f"""
        <div class='bbs-container'>
            <div class='title'>Victory!</div>
            <div class='section'>
                All questions answered.<br>
                Correct: <span class='yellow'>{player.total_correct}</span><br>
                Incorrect: <span class='yellow'>{player.total_incorrect}</span><br>
                Level: <span class='yellow'>{player.level}</span><br>
                HP: <span class='yellow'>{player.hit_points}/{player.max_hit_points}</span><br>
                Weapon: <span class='yellow'>{player.weapon['name']}</span><br>
                Armor: <span class='yellow'>{player.armor['name']}</span>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=victory_html)]

    def show_game_over(self, player: Player):
        game_over_html = f"""
        <div class='bbs-container'>
            <div class='title'>Game Over</div>
            <div class='section'>
                Correct: <span class='yellow'>{player.total_correct}</span><br>
                Incorrect: <span class='yellow'>{player.total_incorrect}</span><br>
                Level: <span class='yellow'>{player.level}</span><br>
                HP: <span class='yellow'>{player.hit_points}/{player.max_hit_points}</span><br>
                Weapon: <span class='yellow'>{player.weapon['name']}</span><br>
                Armor: <span class='yellow'>{player.armor['name']}</span>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=game_over_html)]

# **Controller**: Ties the UI and model together.
class GameController:
    def __init__(self, questions_data: List[Dict], monsters_data: List[Dict]):
        self.model = GameModel(questions_data, monsters_data)
        self.ui = GameUI()
        self.ui.show_initial_screen(self.start_adventure)

    def start_adventure(self):
        status = self.model.next_encounter()
        self.show_encounter_status(status)

    def show_encounter_status(self, status):
        if status == "victory":
            self.ui.show_victory(self.model.player)
        elif status == "no_questions":
            self.ui.show_no_questions(self.model.player)
        else:
            # Continue normally
            self.ui.show_encounter(
                self.model.player,
                self.model.current_monster,
                self.model.current_question,
                self.submit_answer,
                self.request_hint
            )

    def request_hint(self, hint):
        # This will be called by UI on hint click, but we have direct access to question
        # Actually UI handles showing the hint itself. We just provide it if needed.
        pass

    def submit_answer(self, selected_options):
        if not self.model.current_question:
            return
        if not selected_options:
            # Append a warning in UI
            self.ui.show_hint("Please select at least one option.")
            return
        battle_data = self.model.evaluate_answer(selected_options)
        if battle_data["defeated_player"]:
            self.ui.show_game_over(self.model.player)
            return
        self.ui.show_results(self.model.player, self.model.current_monster, battle_data, self.continue_adventure)

    def continue_adventure(self):
        status = self.model.next_encounter()
        self.show_encounter_status(status)


# **start_game**: Entry point to start the game.
def start_game(questions_file, monsters_file="default"):
    questions_data = load_json(questions_file)
    if monsters_file == "default":
        monsters_file = "https://github.com/brendanpshea/computing_concepts_python/raw/main/lotr/lotr_monsters.json"
    monsters_data = load_json(monsters_file)
    if not questions_data:
        print("Cannot start without questions.")
        return
    if not monsters_data:
        print("Cannot start without monsters.")
        return
    GameController(questions_data, monsters_data)
