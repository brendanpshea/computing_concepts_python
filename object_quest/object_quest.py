## object_quest.py
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
import unittest
import traceback
import json
from typing import Dict, List, Any

class QuestSystem:
    def __init__(self, quest_file: str = 'quests.json'):
        self.quests = self.load_quests(quest_file)
        self.current_quest_idx = 0
        self.setup_styles()
        self.create_ui()

    def load_quests(self, quest_file: str) -> List[Dict[str, Any]]:
        with open(quest_file, 'r') as f:
            data = json.load(f)
            return data['quests']

    def setup_styles(self):
        style = """
        <style>
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
        }
        .quest-header {
            background: linear-gradient(135deg, #1a5f7a 0%, #2E86C1 100%);
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin: -20px -20px 20px -20px;
        }
        .quest-number {
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
            color: #BDE3FF;
        }
        .quest-title {
            font-size: 28px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 15px;
        }
        .quest-description {
            font-size: 16px;
            line-height: 1.6;
            color: #eee;
        }
        .test-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #2E86C1;
            margin: 20px 0;
            font-size: 15px;
        }
        .test-header {
            font-weight: bold;
            color: #2E86C1;
            margin-bottom: 15px;
            font-size: 18px;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .test-item {
            color: #34495E;
            margin: 12px 0;
            font-family: 'Courier New', monospace;
            padding: 5px 10px;
            background: #fff;
            border-radius: 4px;
        }
        .code-section {
            margin: 25px 0;
        }
        .code-header {
            font-weight: bold;
            color: #2E86C1;
            margin-bottom: 10px;
            font-size: 18px;
        }
        .error-message {
            color: #E74C3C;
            padding: 15px;
            background-color: #FADBD8;
            border-radius: 8px;
            margin-top: 15px;
            border-left: 4px solid #E74C3C;
        }
        .success-message {
            color: #27AE60;
            padding: 20px;
            background-color: #D4EFDF;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
            border: 2px solid #27AE60;
            font-size: 18px;
        }
        .hint-message {
            color: #8E44AD;
            padding: 15px;
            background-color: #F5EEF8;
            border-radius: 8px;
            margin-top: 15px;
            border-left: 4px solid #8E44AD;
        }
        .success-screen {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
            color: white;
            border-radius: 8px;
            margin: 20px 0;
        }
        .success-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .success-text {
            font-size: 18px;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        </style>
        """
        display(HTML(style))


    def create_ui(self):
        clear_output(wait=True)
        quest = self.quests[self.current_quest_idx]

        display(HTML(f"""
        <div class="container">
            <div class="quest-header">
                <div class="quest-number"><h2>Quest {self.current_quest_idx + 1} : {quest['title']}</h2></div>
                <div class="quest-description"><br><em>{quest['description']}</em></div>
            </div>
        """))

        display(HTML('<div class="code-section"><div class="code-header"><br>✍️ Write your code here:</div></div>'))

        self.code_input = widgets.Textarea(
            value=quest['initial_code'],
            layout=widgets.Layout(width='100%', height='200px', font_family='monospace')
        )
        display(self.code_input)

        submit_button = widgets.Button(
            description='⚔️ Submit Quest',
            button_style='success',
            layout=widgets.Layout(margin='10px 10px 10px 0px')
        )
        submit_button.on_click(self.check_solution)

        hint_button = widgets.Button(
            description='💡 Get Hint',
            button_style='info',
            layout=widgets.Layout(margin='10px 0px 10px 0px')
        )
        hint_button.on_click(self.show_hint)

        button_box = widgets.HBox([submit_button, hint_button])
        display(button_box)
        display(HTML('</div>'))

    def show_success_screen(self, quest):
        clear_output(wait=True)

        display(HTML(f"""
        <div class="container">
            <div class="success-screen">
                <div class="success-title">🎉 Victory!</div>
                <div class="success-text">{quest['success_message']}</div>
            </div>
        """))

        if self.current_quest_idx < len(self.quests) - 1:
            next_button = widgets.Button(
                description='➡️ Continue to Next Quest',
                button_style='success',
                layout=widgets.Layout(width='200px')
            )
            next_button.on_click(lambda _: self.advance_to_next_quest())
            display(next_button)
        else:
            display(HTML("""
                <div class="success-text">
                    Congratulations! You've completed all quests!
                    You are now a true Coding Warrior! 🏆
                </div>
            """))
        display(HTML('</div>'))

    def advance_to_next_quest(self):
        self.current_quest_idx += 1
        self.create_ui()

    def check_solution(self, _):
        try:
            exec(self.code_input.value, globals())
            exec(self.quests[self.current_quest_idx]['test_code'], globals())
            test_class_name = self.quests[self.current_quest_idx]['test_code'].split('class ')[1].split('(')[0]
            test_class = globals()[test_class_name]
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            result = unittest.TextTestRunner(stream=None).run(suite)

            if result.wasSuccessful():
                self.show_success_screen(self.quests[self.current_quest_idx])
            else:
                display(HTML("""
                <div class='error-message'>
                    ⚠️ Not quite there yet, brave coder! Check the error messages below:
                </div>
                """))
                for failure in result.failures:
                    print(failure[1])

        except Exception as e:
            display(HTML(f"""
            <div class='error-message'>
                ⚠️ Your code encountered an error:
                <pre>{str(e)}</pre>
                <pre>{traceback.format_exc()}</pre>
            </div>
            """))

    def show_hint(self, _):
        quest = self.quests[self.current_quest_idx]
        if quest['hints']:
            display(HTML(f"""
            <div class='hint-message'>
                💡 Hint: {quest['hints'][0]}
            </div>
            """))
