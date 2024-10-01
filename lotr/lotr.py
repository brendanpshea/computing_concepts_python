import json
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# ----------------------------
# Utility Functions and Data
# ----------------------------

def load_json(file_path_or_url: str) -> List[Dict]:
    """
    Load JSON data from a local file or a URL with error handling.
    """
    import requests
    import os
    try:
        if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
            # Load from URL
            response = requests.get(file_path_or_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            print(f"Loaded {len(data)} items from URL '{file_path_or_url}'.")
        elif os.path.isfile(file_path_or_url):
            # Load from local file
            with open(file_path_or_url, 'r') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} items from file '{file_path_or_url}'.")
        else:
            print(f"Error: '{file_path_or_url}' is neither a valid file nor a URL.")
            return []
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path_or_url}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file or URL '{file_path_or_url}' contains invalid JSON.")
        return []
    except requests.RequestException as e:
        print(f"Error: Failed to load data from URL '{file_path_or_url}'. Reason: {e}")
        return []

# Weapons and Armor Data
WEAPONS = {
    "Fists": {"name": "Fists", "attack_die": 4, "price": 0},
    "Dagger": {"name": "Dagger", "attack_die": 6, "price": 20},
    "Sword": {"name": "Sword", "attack_die": 8, "price": 50},
    "Greatsword": {"name": "Greatsword", "attack_die": 10, "price": 100},
    # Add more weapons as needed
}

ARMORS = {
    "Clothes": {"name": "Clothes", "defense": 0, "price": 0},
    "Leather Armor": {"name": "Leather Armor", "defense": 2, "price": 20},
    "Chainmail": {"name": "Chainmail", "defense": 4, "price": 50},
    "Plate Armor": {"name": "Plate Armor", "defense": 6, "price": 100},
    # Add more armors as needed
}

# ----------------------------
# CSS Styles
# ----------------------------

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
.bold {
    font-weight: bold;
}
.underline {
    text-decoration: underline;
}
.yellow {
    color: #ffff00;
}
.red {
    color: #ff0000;
}
.green {
    color: #00ff00;
}
.cyan {
    color: #00ffff;
}
.info {
    color: #00ced1;
}
.button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}
</style>
"""

# ----------------------------
# Data Classes
# ----------------------------

@dataclass
class Player:
    hit_points: int = 10
    weapon: Dict[str, Union[str, int]] = field(default_factory=lambda: WEAPONS["Fists"])
    armor: Dict[str, Union[str, int]] = field(default_factory=lambda: ARMORS["Clothes"])
    gold: int = 0
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
    gold_value: int = field(init=False)

    def __post_init__(self):
        self.hit_points = sum(random.randint(1, 6) for _ in range(self.hit_dice))
        self.gold_value = random.randint(1, self.hit_dice * 6)

# ----------------------------
# Game Class
# ----------------------------

class Game:
    def __init__(self, questions_data: Optional[List[Dict]] = None, monsters_data: Optional[List[Dict]] = None):
        # Load CSS Styles
        display(HTML(BBS_CSS))
        
        # Load data
        if questions_data is None:
            self.questions = []
            print("Warning: No questions data provided.")
        else:
            self.questions = questions_data
        if monsters_data is None:
            self.monsters_data = []
            print("Warning: No monsters data provided.")
        else:
            # Calculate difficulty score and sort monsters
            difficulty_monsters = []
            for monster in monsters_data:
                difficulty_score = monster['hit_dice'] + monster['attack_die'] + monster['defense']
                difficulty_monsters.append((difficulty_score, monster))
            # Sort monsters by difficulty_score
            sorted_monsters = sorted(difficulty_monsters, key=lambda x: x[0])
            # Extract the sorted monsters
            self.monsters_data = [monster for _, monster in sorted_monsters]
        
        # Initialize Player
        self.player = Player()

        # Shuffle questions at the start
        random.shuffle(self.questions)
        self.questions_to_ask = self.questions.copy()

        self.current_monster: Optional[Monster] = None
        self.current_question: Optional[Dict] = None

        # Initialize counters and flags
        self.questions_asked = 0
        self.STORE_INTERVAL = 3  # The store will appear after every 3 questions
        self.store_message = widgets.HTML(value="")
        self.gold_label = widgets.HTML(value="")
        self.just_visited_store = False  # Initialize the flag

        # Setup UI
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

        # Render the initial game state
        self.render_initial_screen()

    def render_initial_screen(self):
        """
        Render the initial screen before any encounters.
        """
        initial_html = f"""
        <div class='bbs-container'>
            <div class='title'>Welcome to the Loop of the Recursive Dragon!</div>
            <div class='section'>
                Prepare yourself for a challenging quiz adventure. Answer questions correctly to defeat monsters and earn gold. Visit the store after every {self.STORE_INTERVAL} questions to upgrade your equipment.
            </div>
            <div class='section'>
                <button class='button' onclick="{self.present_encounter.__name__}()">Start Adventure</button>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=initial_html)]

    def generate_monster(self) -> Optional[Monster]:
        """
        Generate a monster appropriate for the player's progression.
        """
        if not self.monsters_data:
            print("Error: No monsters data available.")
            return None

        # Constants for progression
        QUESTIONS_PER_STAGE = 3  # Number of questions per stage
        TOTAL_STAGES = 5  # Define the number of stages you want
        monsters_per_stage = max(len(self.monsters_data) // TOTAL_STAGES, 1)

        # Calculate current stage based on questions answered
        current_stage = min(self.questions_asked // QUESTIONS_PER_STAGE, TOTAL_STAGES - 1)

        # Determine the index range of monsters for the current stage
        max_monster_index = min((current_stage + 1) * monsters_per_stage, len(self.monsters_data))

        # Create the pool of monsters for the current stage
        available_monsters = self.monsters_data[:max_monster_index]

        # Select a random monster from available options
        data = random.choice(available_monsters)
        monster = Monster(
            monster_name=data["monster_name"],
            initial_description=data.get("initial_description", ""),
            hit_dice=data["hit_dice"],
            attack_die=data["attack_die"],
            defense=data["defense"]
        )
        return monster

    def present_encounter(self):
        """
        Present a monster encounter and a question to the player.
        If a monster is already being battled and has HP remaining, continue battling it.
        """
        # If there's no current monster or the current monster has been defeated, generate a new one
        if not self.current_monster or self.current_monster.hit_points <= 0:
            if not self.questions_to_ask:
                self.show_victory()
                return
            self.current_monster = self.generate_monster()
            self.initial_encounter = True
        else:
            self.initial_encounter = False

        # Select the next question
        if self.questions_to_ask:
            self.current_question = self.questions_to_ask.pop(0)
        else:
            self.current_question = None  # No question available

        # Remove debug print statements
        # if self.current_question:
        #     print(f"Presenting question: {self.current_question.get('question', 'No question key found.')}")

        # Build the encounter and question HTML
        if self.initial_encounter:
            encounter_html = f"""
            <div class='bbs-container'>
                <div class='title'>Loop of the Recursive Dragon</div>
                <div class='section'>
                    You encounter a <span class='bold underline'>{self.current_monster.monster_name}</span>! {self.current_monster.initial_description}<br>
                    It has <span class='yellow'>{self.current_monster.hit_points}</span> HP.<br>
                    You have <span class='yellow'>{self.player.hit_points}</span> HP, wielding a <span class='yellow'>{self.player.weapon['name']}</span> and wearing <span class='yellow'>{self.player.armor['name']}</span>.
                </div>
            </div>
            """
        else:
            encounter_html = f"""
            <div class='bbs-container'>
                <div class='title'>Loop of the Recursive Dragon</div>
                <div class='section'>
                    You are still battling the <span class='bold underline'>{self.current_monster.monster_name}</span>!<br>
                    It has <span class='yellow'>{self.current_monster.hit_points}</span> HP remaining.<br>
                    You have <span class='yellow'>{self.player.hit_points}</span> HP, wielding a <span class='yellow'>{self.player.weapon['name']}</span> and wearing <span class='yellow'>{self.player.armor['name']}</span>.
                </div>
            </div>
            """

        if self.current_question:
            encounter_html += f"""
                <div class='bbs-container'>
                    <div class='section'>
                        <span class='bold'>Question:</span> {self.current_question['question']}
                    </div>
                </div>
            """
        else:
            # Monster flees if no more questions but still alive
            encounter_html += f"""
                <div class='bbs-container'>
                    <div class='section'>
                        <span class='bold red'>All questions have been answered!</span> The <span class='bold underline'>{self.current_monster.monster_name}</span> flees.
                    </div>
                    <div class='section'>
                        <span class='bold'>Final Stats:</span><br>
                        Correct Answers: <span class='yellow'>{self.player.total_correct}</span><br>
                        Incorrect Answers: <span class='yellow'>{self.player.total_incorrect}</span><br>
                        HP: <span class='yellow'>{self.player.hit_points}</span><br>
                        Gold: <span class='yellow'>{self.player.gold}</span><br>
                        Weapon: <span class='yellow'>{self.player.weapon['name']}</span><br>
                        Armor: <span class='yellow'>{self.player.armor['name']}</span>
                    </div>
                </div>
            """

        # Prepare answer options
        if self.current_question:
            options = self.current_question.get('correct', []) + self.current_question.get('incorrect', [])
            random.shuffle(options)
        else:
            options = []

        # Create Checkboxes for options with adjusted styles to allow text wrapping
        self.checkboxes = [
            widgets.Checkbox(
                value=False,
                description=opt,
                indent=False,
                style={'description_width': 'initial'},  # Allows the description to take full width
                layout=widgets.Layout(width='100%')     # Ensures the checkbox takes full container width
            )
            for opt in options
        ]

        # Adjust the VBox to accommodate wider checkboxes and enable scrolling if necessary
        checkboxes_box = widgets.VBox(
            self.checkboxes,
            layout=widgets.Layout(overflow_y='auto', max_height='300px', width='100%')  # Increased max_height and set width to 100%
        )

        # Create Buttons
        submit_button = widgets.Button(description="Submit Answer", button_style='success')
        hint_button = widgets.Button(description="Show Hint", button_style='info')
        submit_button.on_click(self.on_submit)
        hint_button.on_click(self.on_hint)

        buttons_box = widgets.HBox(
            [submit_button, hint_button],
            layout=widgets.Layout(justify_content='center', gap='10px', width='100%')  # Ensures buttons are centered
        )

        # Update the main container with new content
        if self.current_question:
            self.main_container.children = [
                widgets.HTML(value=encounter_html),
                checkboxes_box,
                buttons_box
                # widgets.HTML(value="")  # Placeholder for output messages
            ]
        else:
            # If no more questions, end the game
            self.main_container.children = [
                widgets.HTML(value=encounter_html)
            ]

    def on_submit(self, b):
        """
        Handle the submission of an answer.
        """
        if not self.current_question:
            error_html = f"<div class='bbs-container'><div class='section'><span class='red bold'>No question to answer.</span></div></div>"
            self.main_container.children += (widgets.HTML(value=error_html),)
            return

        # Collect selected options from the checkboxes
        selected_options = [cb.description for cb in self.checkboxes if cb.value]
        if not selected_options:
            warning_html = f"<div class='bbs-container'><div class='section'><span class='cyan'>Please select at least one option.</span></div></div>"
            self.main_container.children += (widgets.HTML(value=warning_html),)
            return

        self.evaluate_answer(selected_options)

    def on_hint(self, b):
        """
        Provide a hint for the current question.
        """
        if not self.current_question:
            hint_html = f"<div class='bbs-container'><div class='section'><span class='red'>No question available for a hint.</span></div></div>"
        else:
            hint = self.current_question.get('hint', 'No hint available.')
            hint_html = f"<div class='bbs-container'><div class='section'><span class='cyan'>Hint: {hint}</span></div></div>"

        # Display the hint below the buttons
        # Check if there's already a hint message and replace it
        if len(self.main_container.children) >= 3:
            # Replace the third widget if it's a hint
            if isinstance(self.main_container.children[2], widgets.HBox):
                # Insert hint after the buttons
                new_children = list(self.main_container.children)
                # Remove existing hint if any
                if len(new_children) > 3:
                    new_children.pop(3)
                # Add the new hint
                new_children.insert(3, widgets.HTML(value=hint_html))
                self.main_container.children = tuple(new_children)
            else:
                # Just append the hint
                self.main_container.children += (widgets.HTML(value=hint_html),)
        else:
            # Append the hint
            self.main_container.children += (widgets.HTML(value=hint_html),)

    def evaluate_answer(self, selected_options: List[str]):
        """
        Evaluate the player's answer and update game state accordingly.
        """
        correct_set = set(self.current_question.get('correct', []))
        incorrect_set = set(self.current_question.get('incorrect', []))
        selected_set = set(selected_options)

        # Determine correct and incorrect selections
        correct_selections = selected_set & correct_set
        incorrect_selections = selected_set & incorrect_set
        missed_correct = correct_set - selected_set

        # Update total correct and incorrect counters
        self.player.total_correct += len(correct_selections)
        self.player.total_incorrect += len(incorrect_selections)

        # Calculate Damage to Monster
        player_hits = len(correct_selections)
        player_damage = sum(random.randint(1, self.player.weapon['attack_die']) for _ in range(player_hits))
        effective_player_damage = max(player_damage - self.current_monster.defense, 0)
        self.current_monster.hit_points -= effective_player_damage

        # Calculate Damage to Player
        monster_hits = len(incorrect_selections)
        monster_damage = sum(random.randint(1, self.current_monster.attack_die) for _ in range(monster_hits))
        effective_monster_damage = max(monster_damage - self.player.armor['defense'], 0)
        self.player.hit_points -= effective_monster_damage

        # Build Battle Results
        battle_results = "<div class='bbs-container'><div class='section'>"

        if effective_player_damage > 0:
            battle_results += f"You attack the <span class='bold'>{self.current_monster.monster_name}</span> with your <span class='yellow'>{self.player.weapon['name']}</span> and deal <span class='yellow'>{effective_player_damage}</span> damage.<br>"
        else:
            battle_results += f"Your attack couldn't penetrate the <span class='bold'>{self.current_monster.monster_name}</span>'s defense.<br>"

        if effective_monster_damage > 0:
            battle_results += f"The <span class='bold'>{self.current_monster.monster_name}</span> retaliates and deals <span class='red'>{effective_monster_damage}</span> damage to you due to incorrect answers.<br>"
        else:
            if monster_hits > 0:
                battle_results += f"The <span class='bold'>{self.current_monster.monster_name}</span>'s attack couldn't penetrate your <span class='yellow'>{self.player.armor['name']}</span>.<br>"
            else:
                battle_results += "You avoided all incorrect options. The monster couldn't counter-attack.<br>"

        # Monster Defeated
        if self.current_monster.hit_points <= 0:
            battle_results += f"<span class='bold'>You have defeated the {self.current_monster.monster_name}!</span><br>"
            self.player.gold += self.current_monster.gold_value
            battle_results += f"You collect <span class='yellow'>{self.current_monster.gold_value}</span> gold pieces.<br>"
            battle_results += f"Total gold: <span class='yellow'>{self.player.gold}</span>.<br>"
        else:
            battle_results += f"The <span class='bold'>{self.current_monster.monster_name}</span> has <span class='yellow'>{self.current_monster.hit_points}</span> HP remaining.<br>"

        # Player Defeated
        if self.player.hit_points <= 0:
            battle_results += f"<span class='red bold'>You have been defeated! Game Over.</span></div></div>"
            self.main_container.children = [
                widgets.HTML(value=battle_results)
            ]
            return

        # Player Status
        battle_results += f"Your current HP: <span class='yellow'>{self.player.hit_points}</span>.<br>"

        # Re-add question if not perfectly answered
        if missed_correct or incorrect_selections:
            self.questions_to_ask.append(self.current_question)
            battle_results += "<span class='cyan'>You didn't answer perfectly. The question will come up again later.</span><br>"

        battle_results += "</div></div>"

        # Increment the number of questions asked
        self.questions_asked += 1

        # Decide whether to present the store or the next encounter
        if self.questions_asked % self.STORE_INTERVAL == 0 and self.questions_asked > 0:
            self.present_store()
            return

        # Display the battle results and a continue button
        continue_button = widgets.Button(description="Continue", button_style='primary', layout=widgets.Layout(width='150px'))
        continue_button.on_click(lambda b: self.present_encounter())
        self.main_container.children = [
            widgets.HTML(value=battle_results),
            continue_button
        ]

    def present_store(self):
        """
        Present the store to the player where they can buy items.
        """
        self.just_visited_store = True  # Set the flag
        store_html = f"""
        <div class='bbs-container'>
            <div class='title'>The Traveling Merchant</div>
            <div class='section'>
                A mysterious merchant appears and offers you goods for sale.
            </div>
        </div>
        """

        # Update the gold label
        self.gold_label.value = f"You have <span class='yellow'>{self.player.gold}</span> gold."

        # Create a list to hold all items for sale
        items_for_sale = []

        # Add weapons to items for sale
        for weapon_name, weapon in WEAPONS.items():
            # Skip the starting weapon (Fists) or any items the player already has
            if weapon_name == "Fists" or weapon_name == self.player.weapon['name']:
                continue
            items_for_sale.append({
                "name": weapon['name'],
                "type": "weapon",
                "price": weapon['price'],
                "stats": f"Atk Die: {weapon['attack_die']}"
            })

        # Add armors to items for sale
        for armor_name, armor in ARMORS.items():
            # Skip the starting armor (Clothes) or any items the player already has
            if armor_name == "Clothes" or armor_name == self.player.armor['name']:
                continue
            items_for_sale.append({
                "name": armor['name'],
                "type": "armor",
                "price": armor['price'],
                "stats": f"Defense: {armor['defense']}"
            })

        # Add potions or other consumables
        items_for_sale.append({
            "name": "Health Potion",
            "type": "potion",
            "price": 20,
            "effect": "heal",
            "value": 10,
            "stats": "+10 HP"
        })

        # Create widgets to display items and allow purchase
        item_widgets = []
        for item in items_for_sale:
            # Create a label for the item
            item_label = widgets.HTML(
                value=f"<div style='display: flex; align-items: center; width: 600px;'>"
                      f"<span style='flex: 1; font-size:14px; word-wrap: break-word;'>{item['name']} ({item['stats']}) "
                      f"(<span class='yellow'>{item['price']}</span> gold)</span>"
                      f"</div>"
            )
            # Create a buy button
            buy_button = widgets.Button(
                description="Buy",
                button_style='primary',
                layout=widgets.Layout(width='80px')
            )
            # Disable button if player can't afford or already owns the item
            if self.player.gold < item['price'] or (
                (item['type'] == 'weapon' and item['name'] == self.player.weapon['name']) or
                (item['type'] == 'armor' and item['name'] == self.player.armor['name'])
            ):
                buy_button.disabled = True

            # Capture the current item in the lambda
            buy_button.on_click(lambda b, item=item: self.buy_item(item))
            # Combine label and button in a horizontal box
            item_row = widgets.HBox([item_label, buy_button], layout=widgets.Layout(gap='10px'))
            item_widgets.append(item_row)

        # Create a container for the item widgets
        items_box = widgets.VBox(item_widgets, layout=widgets.Layout(gap='10px', overflow_y='auto', max_height='400px'))

        # Create a button to continue the adventure
        continue_button = widgets.Button(
            description="Continue Adventure",
            button_style='success',
            layout=widgets.Layout(width='200px')
        )
        continue_button.on_click(lambda b: self.game_loop())

        # Update the main container
        self.main_container.children = [
            widgets.HTML(value=store_html),
            self.gold_label,
            items_box,
            self.store_message,
            continue_button
        ]

    def buy_item(self, item):
        """
        Handle the purchase of an item.
        """
        if self.player.gold < item['price']:
            # Not enough gold
            message = f"<div class='bbs-container'><div class='section'><span class='red'>You do not have enough gold to buy {item['name']}.</span></div></div>"
        else:
            self.player.gold -= item['price']
            if item['type'] == 'potion':
                # Heal the player
                self.player.hit_points += item['value']
                message = f"<div class='bbs-container'><div class='section'><span class='cyan'>You purchased {item['name']} and healed {item['value']} HP.</span></div></div>"
            elif item['type'] == 'weapon':
                # Update the player's weapon
                self.player.weapon = WEAPONS[item['name']]
                message = f"<div class='bbs-container'><div class='section'><span class='cyan'>You purchased and equipped {item['name']}.</span></div></div>"
            elif item['type'] == 'armor':
                # Update the player's armor
                self.player.armor = ARMORS[item['name']]
                message = f"<div class='bbs-container'><div class='section'><span class='cyan'>You purchased and equipped {item['name']}.</span></div></div>"
            else:
                message = f"<div class='bbs-container'><div class='section'><span class='red'>Error: Unknown item type.</span></div></div>"

            # Update the gold label
            self.gold_label.value = f"You have <span class='yellow'>{self.player.gold}</span> gold."

        # Update the message
        self.store_message.value = message

        # Refresh the store to update button states
        self.present_store()

    def show_victory(self):
        """
        Display the victory screen when all questions are answered.
        """
        victory_html = f"""
        <div class='bbs-container'>
            <div class='title'>Victory!</div>
            <div class='section'>
                Congratulations! You have answered all questions and defeated all monsters.<br>
                <span class='bold'>Final Stats:</span><br>
                Correct Answers: <span class='yellow'>{self.player.total_correct}</span><br>
                Incorrect Answers: <span class='yellow'>{self.player.total_incorrect}</span><br>
                HP: <span class='yellow'>{self.player.hit_points}</span><br>
                Gold: <span class='yellow'>{self.player.gold}</span><br>
                Weapon: <span class='yellow'>{self.player.weapon['name']}</span><br>
                Armor: <span class='yellow'>{self.player.armor['name']}</span>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=victory_html)]

    def show_game_over(self):
        """
        Display the game over screen when the player is defeated.
        """
        game_over_html = f"""
        <div class='bbs-container'>
            <div class='title'>Game Over</div>
            <div class='section'>
                You have been defeated by the <span class='bold underline'>{self.current_monster.monster_name}</span>.<br>
                <span class='bold'>Final Stats:</span><br>
                Correct Answers: <span class='yellow'>{self.player.total_correct}</span><br>
                Incorrect Answers: <span class='yellow'>{self.player.total_incorrect}</span><br>
                HP: <span class='yellow'>{self.player.hit_points}</span><br>
                Gold: <span class='yellow'>{self.player.gold}</span><br>
                Weapon: <span class='yellow'>{self.player.weapon['name']}</span><br>
                Armor: <span class='yellow'>{self.player.armor['name']}</span>
            </div>
        </div>
        """
        self.main_container.children = [widgets.HTML(value=game_over_html)]

    def game_loop(self):
        """
        Main game loop to handle game progression.
        """
        if self.player.hit_points <= 0:
            self.show_game_over()
            return
        if not self.questions_to_ask and not self.current_monster:
            self.show_victory()
            return
        # Check if it's time to show the store
        if (self.questions_asked % self.STORE_INTERVAL == 0 and
                self.questions_asked > 0 and not self.just_visited_store):
            self.present_store()
        else:
            self.just_visited_store = False  # Reset the flag
            self.present_encounter()

    def evaluate_answer(self, selected_options: List[str]):
        """
        Evaluate the player's answer and update game state accordingly.
        """
        correct_set = set(self.current_question.get('correct', []))
        incorrect_set = set(self.current_question.get('incorrect', []))
        selected_set = set(selected_options)

        # Determine correct and incorrect selections
        correct_selections = selected_set & correct_set
        incorrect_selections = selected_set & incorrect_set
        missed_correct = correct_set - selected_set

        # Update total correct and incorrect counters
        self.player.total_correct += len(correct_selections)
        self.player.total_incorrect += len(incorrect_selections)

        # Calculate Damage to Monster
        player_hits = len(correct_selections)
        player_damage = sum(random.randint(1, self.player.weapon['attack_die']) for _ in range(player_hits))
        effective_player_damage = max(player_damage - self.current_monster.defense, 0)
        self.current_monster.hit_points -= effective_player_damage

        # Calculate Damage to Player
        monster_hits = len(incorrect_selections)
        monster_damage = sum(random.randint(1, self.current_monster.attack_die) for _ in range(monster_hits))
        effective_monster_damage = max(monster_damage - self.player.armor['defense'], 0)
        self.player.hit_points -= effective_monster_damage

        # Build Battle Results
        battle_results = "<div class='bbs-container'><div class='section'>"

        if effective_player_damage > 0:
            battle_results += f"You attack the <span class='bold'>{self.current_monster.monster_name}</span> with your <span class='yellow'>{self.player.weapon['name']}</span> and deal <span class='yellow'>{effective_player_damage}</span> damage.<br>"
        else:
            battle_results += f"Your attack couldn't penetrate the <span class='bold'>{self.current_monster.monster_name}</span>'s defense.<br>"

        if effective_monster_damage > 0:
            battle_results += f"The <span class='bold'>{self.current_monster.monster_name}</span> retaliates and deals <span class='red'>{effective_monster_damage}</span> damage to you due to incorrect answers.<br>"
        else:
            if monster_hits > 0:
                battle_results += f"The <span class='bold'>{self.current_monster.monster_name}</span>'s attack couldn't penetrate your <span class='yellow'>{self.player.armor['name']}</span>.<br>"
            else:
                battle_results += "You avoided all incorrect options. The monster couldn't counter-attack.<br>"

        # Monster Defeated
        if self.current_monster.hit_points <= 0:
            battle_results += f"<span class='bold'>You have defeated the {self.current_monster.monster_name}!</span><br>"
            self.player.gold += self.current_monster.gold_value
            battle_results += f"You collect <span class='yellow'>{self.current_monster.gold_value}</span> gold pieces.<br>"
            battle_results += f"Total gold: <span class='yellow'>{self.player.gold}</span>.<br>"
        else:
            battle_results += f"The <span class='bold'>{self.current_monster.monster_name}</span> has <span class='yellow'>{self.current_monster.hit_points}</span> HP remaining.<br>"

        # Player Defeated
        if self.player.hit_points <= 0:
            battle_results += f"<span class='red bold'>You have been defeated! Game Over.</span></div></div>"
            self.main_container.children = [
                widgets.HTML(value=battle_results)
            ]
            return

        # Player Status
        battle_results += f"Your current HP: <span class='yellow'>{self.player.hit_points}</span>.<br>"

        # Re-add question if not perfectly answered
        if missed_correct or incorrect_selections:
            self.questions_to_ask.append(self.current_question)
            battle_results += "<span class='cyan'>You didn't answer perfectly. The question will come up again later.</span><br>"

        battle_results += "</div></div>"

        # Increment the number of questions asked
        self.questions_asked += 1

        # Decide whether to present the store or the next encounter
        if self.questions_asked % self.STORE_INTERVAL == 0 and self.questions_asked > 0:
            self.present_store()
            return

        # Display the battle results and a continue button
        continue_button = widgets.Button(description="Continue", button_style='primary', layout=widgets.Layout(width='150px'))
        continue_button.on_click(lambda b: self.present_encounter())
        self.main_container.children = [
            widgets.HTML(value=battle_results),
            continue_button
        ]

# ----------------------------
# Function to Start the Game
# ----------------------------

def start_game(questions_file: str, monsters_file: str):
    """
    Start the quiz game using the provided questions and monsters JSON files.
    The files can be local file paths or URLs.
    """
    # Load questions and monsters data
    questions_data = load_json(questions_file)
    monsters_data = load_json(monsters_file)

    # Check if data was loaded successfully
    if not questions_data:
        print("Cannot start the game without questions.")
        return
    if not monsters_data:
        print("Cannot start the game without monsters.")
        return

    # Initialize and start the game
    game = Game(questions_data=questions_data, monsters_data=monsters_data)
