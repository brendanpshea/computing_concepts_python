# lotr_.py

import json
import random
import os
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import ipywidgets as widgets
from IPython.display import display, HTML


# **Utility Functions**
# **load_json(file_path_or_url)**: Loads **JSON** data. Returns empty if fails.
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

# CSS
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

# **Data Classes**
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
    xp_value: int = field(init=False)  # XP value based on hd

    def __post_init__(self):
        # Monster hit points: sum of hd d6 rolls
        self.hit_points = sum(random.randint(1, 6) for _ in range(self.hit_dice))
        # XP is, for simplicity, hd * 10
        self.xp_value = self.hit_dice * 10

# **Game Class**
class Game:
    def __init__(self, questions_data: Optional[List[Dict]] = None, monsters_data: Optional[List[Dict]] = None):
        display(HTML(BBS_CSS))
        self.questions = questions_data if questions_data else []
        self.monsters_data = monsters_data if monsters_data else []
        self.player = Player()

        random.shuffle(self.questions)
        self.questions_to_ask = self.questions.copy()

        self.current_monster: Optional[Monster] = None
        self.current_question: Optional[Dict] = None
        self.questions_asked = 0
        self.initial_encounter = True

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
        display(self.main_container)
        self.render_initial_screen()

    def render_initial_screen(self):
        start_button = widgets.Button(
            description="Start Adventure",
            button_style='success',
            layout=widgets.Layout(width='200px', height='40px')
        )
        start_button.on_click(lambda b: self.present_encounter())

        initial_html = f"""
        <div class='bbs-container'>
            <div class='title'>Welcome to the Loop of the Recursive Dragon!</div>
            <div class='section'>
                Face monsters with hit dice close to your level. Answer questions correctly to deal damage. Gain XP and level up after enough victories. Upon leveling up, your health and gear improve automatically.
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=initial_html), start_button]

    def generate_monster(self) -> Optional[Monster]:
        if not self.monsters_data:
            print("Error: No monsters data available.")
            return None

        # Player fights monsters within ±1 hd of current level.
        valid_monsters = [m for m in self.monsters_data if abs(m['hit_dice'] - self.player.level) <= 1]
        if not valid_monsters:
            # If none available, just pick any monster
            valid_monsters = self.monsters_data

        selected_monster_data = random.choice(valid_monsters)
        return Monster(
            monster_name=selected_monster_data["monster_name"],
            initial_description=selected_monster_data.get("initial_description", ""),
            hit_dice=selected_monster_data["hit_dice"],
            attack_die=selected_monster_data["attack_die"],
            defense=selected_monster_data["defense"]
        )

    def build_encounter_html(self) -> str:
        if self.initial_encounter:
            intro = f"You encounter a <span class='bold underline'>{self.current_monster.monster_name}</span>! {self.current_monster.initial_description}"
        else:
            intro = f"You are still battling the <span class='bold underline'>{self.current_monster.monster_name}</span>!"
        encounter_html = f"""
        <div class='bbs-container'>
            <div class='title'>Loop of the Recursive Dragon</div>
            <div class='section'>
                {intro}<br>
                It has <span class='yellow'>{self.current_monster.hit_points}</span> HP.<br>
                You have <span class='yellow'>{self.player.hit_points}</span>/<span class='yellow'>{self.player.max_hit_points}</span> HP.
                Level: <span class='yellow'>{self.player.level}</span>, XP: <span class='yellow'>{self.player.xp}/{self.player.xp_to_next_level}</span><br>
                Weapon: <span class='yellow'>{self.player.weapon['name']}</span>, Armor: <span class='yellow'>{self.player.armor['name']}</span>
            </div>
        </div>
        """
        return encounter_html

    def present_encounter(self):
        if not self.current_monster or self.current_monster.hit_points <= 0:
            if not self.questions_to_ask:
                self.show_victory()
                return
            self.current_monster = self.generate_monster()
            self.initial_encounter = True
        else:
            self.initial_encounter = False

        self.current_question = self.questions_to_ask.pop(0) if self.questions_to_ask else None
        encounter_html = self.build_encounter_html()

        if self.current_question:
            encounter_html += f"""
                <div class='bbs-container'>
                    <div class='section'>
                        <span class='bold'>Question:</span> {self.current_question['question']}
                    </div>
                </div>
            """
            options = self.current_question.get('correct', []) + self.current_question.get('incorrect', [])
            random.shuffle(options)
            self.checkboxes = [widgets.Checkbox(value=False, description=opt, indent=False,
                                                style={'description_width': 'initial'},
                                                layout=widgets.Layout(width='100%'))
                               for opt in options]

            submit_button = widgets.Button(description="Submit Answer", button_style='success')
            hint_button = widgets.Button(description="Show Hint", button_style='info')
            submit_button.on_click(self.on_submit)
            hint_button.on_click(self.on_hint)

            self.main_container.children = [
                widgets.HTML(value=encounter_html),
                widgets.VBox(self.checkboxes, layout=widgets.Layout(overflow_y='auto', max_height='300px', width='100%')),
                widgets.HBox([submit_button, hint_button], layout=widgets.Layout(justify_content='center', gap='10px', width='100%'))
            ]
        else:
            encounter_html += f"""
                <div class='bbs-container'>
                    <div class='section'>
                        <span class='bold red'>All questions have been answered!</span> The <span class='bold underline'>{self.current_monster.monster_name}</span> flees.
                    </div>
                    <div class='section'>
                        <span class='bold'>Final Stats:</span><br>
                        Correct: <span class='yellow'>{self.player.total_correct}</span><br>
                        Incorrect: <span class='yellow'>{self.player.total_incorrect}</span><br>
                        HP: <span class='yellow'>{self.player.hit_points}</span><br>
                        Level: <span class='yellow'>{self.player.level}</span>
                    </div>
                </div>
            """
            self.main_container.children = [widgets.HTML(value=encounter_html)]

    def on_submit(self, b):
        if not self.current_question:
            self.append_html("<div class='bbs-container'><div class='section'><span class='red bold'>No question to answer.</span></div></div>")
            return
        selected = [cb.description for cb in self.checkboxes if cb.value]
        if not selected:
            self.append_html("<div class='bbs-container'><div class='section'><span class='cyan'>Please select at least one option.</span></div></div>")
            return
        self.evaluate_answer(selected)

    def on_hint(self, b):
        if not self.current_question:
            hint_html = "<div class='bbs-container'><div class='section'><span class='red'>No question available for a hint.</span></div></div>"
        else:
            hint = self.current_question.get('hint', 'No hint available.')
            hint_html = f"<div class='bbs-container'><div class='section'><span class='cyan'>Hint: {hint}</span></div></div>"
        self.insert_hint(hint_html)

    def insert_hint(self, hint_html: str):
        children = list(self.main_container.children)
        children = [ch for ch in children if not (isinstance(ch, widgets.HTML) and 'Hint:' in ch.value)]
        children.append(widgets.HTML(value=hint_html))
        self.main_container.children = tuple(children)

    def evaluate_answer(self, selected_options: List[str]):
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

        battle_results = "<div class='bbs-container'><div class='section'>"
        if effective_player_damage > 0:
            battle_results += f"You deal <span class='yellow'>{effective_player_damage}</span> damage.<br>"
        else:
            battle_results += "Your attack was ineffective.<br>"
        if effective_monster_damage > 0:
            battle_results += f"The monster hits you for <span class='red'>{effective_monster_damage}</span> damage.<br>"
        else:
            if monster_hits > 0:
                battle_results += "The monster cannot penetrate your armor.<br>"
            else:
                battle_results += "No counter-attack from the monster.<br>"

        if self.current_monster.hit_points <= 0:
            battle_results += f"<span class='bold'>You defeated {self.current_monster.monster_name}!</span><br>"
            # Award XP
            self.player.xp += self.current_monster.xp_value
            battle_results += f"XP gained: <span class='yellow'>{self.current_monster.xp_value}</span> (Total: {self.player.xp}/{self.player.xp_to_next_level})<br>"
            self.check_level_up()
        else:
            battle_results += f"Monster HP: <span class='yellow'>{self.current_monster.hit_points}</span><br>"

        if self.player.hit_points <= 0:
            battle_results += f"<span class='red bold'>You have been defeated! Game Over.</span></div></div>"
            self.main_container.children = [widgets.HTML(value=battle_results)]
            return

        battle_results += f"Your HP: <span class='yellow'>{self.player.hit_points}/{self.player.max_hit_points}</span><br>"
        if missed_correct or incorrect_selections:
            self.questions_to_ask.append(self.current_question)
            battle_results += "<span class='cyan'>You will face this question again.</span><br>"
        battle_results += "</div></div>"

        self.questions_asked += 1
        continue_button = widgets.Button(description="Continue", button_style='primary', layout=widgets.Layout(width='150px'))
        continue_button.on_click(lambda b: self.present_encounter())
        self.main_container.children = [widgets.HTML(value=battle_results), continue_button]

    def check_level_up(self):
        if self.player.xp >= self.player.xp_to_next_level:
            # Level up
            self.player.level += 1
            # Increase xp requirement for next level 
            self.player.xp_to_next_level = self.player.xp_to_next_level + round(self.player.xp_to_next_level * 1.5)
            # Increase max HP and restore fully
            self.player.max_hit_points += 5
            self.player.hit_points = self.player.max_hit_points
            # Upgrade gear if available
            if self.player.level <= len(WEAPONS):
                self.player.weapon = WEAPONS[self.player.level - 1]
            if self.player.level <= len(ARMORS):
                self.player.armor = ARMORS[self.player.level - 1]

    def show_victory(self):
        victory_html = f"""
        <div class='bbs-container'>
            <div class='title'>Victory!</div>
            <div class='section'>
                All questions answered.<br>
                Correct: <span class='yellow'>{self.player.total_correct}</span><br>
                Incorrect: <span class='yellow'>{self.player.total_incorrect}</span><br>
                Level: <span class='yellow'>{self.player.level}</span><br>
                HP: <span class='yellow'>{self.player.hit_points}/{self.player.max_hit_points}</span><br>
                Weapon: <span class='yellow'>{self.player.weapon['name']}</span><br>
                Armor: <span class='yellow'>{self.player.armor['name']}</span>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=victory_html)]

    def append_html(self, html_str: str):
        children = list(self.main_container.children)
        children.append(widgets.HTML(value=html_str))
        self.main_container.children = tuple(children)

# **start_game**
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
    Game(questions_data=questions_data, monsters_data=monsters_data)
