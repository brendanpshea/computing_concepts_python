# object_quest.py
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
        self.style_loaded = False
        # **Output** pane for all messages
        self.output_area = widgets.Output(layout=widgets.Layout(width='100%'))
        self.setup_styles()
        self.create_ui()

    def load_quests(self, quest_file: str) -> List[Dict[str, Any]]:
        with open(quest_file, 'r') as f:
            data = json.load(f)
        return data['quests']

    def setup_styles(self):
        if self.style_loaded:
            return
        style = """
        <style>
        /* ... same CSS as before ... */
        </style>
        """
        display(HTML(style))
        self.style_loaded = True

    def create_ui(self):
        clear_output(wait=True)
        self.setup_styles()

        quest = self.quests[self.current_quest_idx]

        # **Dropdown** to skip to any quest
        titles = [(f"{i+1}: {q['title']}", i) for i, q in enumerate(self.quests)]
        selector = widgets.Dropdown(options=titles, value=self.current_quest_idx, description='Jump to:')
        selector.observe(self.on_select, names='value')
        display(selector)

        display(HTML(f"""
        <div class="container">
            <div class="quest-header">
                <div class="quest-number"><h2>Quest {self.current_quest_idx + 1}: {quest['title']}</h2></div>
                <div class="quest-description"><em>{quest['description']}</em></div>
            </div>
        """))

        display(HTML('<div class="code-section"><div class="code-header">✍️ Write your code here:</div></div>'))

        self.code_input = widgets.Textarea(
            value=quest['initial_code'],
            layout=widgets.Layout(width='100%', height='200px', font_family='monospace')
        )
        display(self.code_input)

        submit_button = widgets.Button(description='⚔️ Submit Quest', button_style='success')
        submit_button.on_click(self.check_solution)

        hint_button = widgets.Button(description='💡 Get Hint', button_style='info')
        hint_button.on_click(self.show_hint)

        display(widgets.HBox([submit_button, hint_button]))
        display(HTML('</div>'))
        display(self.output_area)

    def on_select(self, change):
        idx = change['new']
        if idx != self.current_quest_idx:
            self.current_quest_idx = idx
            self.output_area.clear_output()
            self.create_ui()

    def check_solution(self, _):
      # clear previous feedback
      self.output_area.clear_output()
      with self.output_area:
          try:
              # prepare an execution namespace with unittest available
              exec_ns: Dict[str, Any] = {
                  '__builtins__': __builtins__,
                  'unittest': unittest
              }

              # run student code
              exec(self.code_input.value, exec_ns, exec_ns)

              # run test definitions
              test_code = self.quests[self.current_quest_idx]['test_code']
              exec(test_code, exec_ns, exec_ns)

              # locate and instantiate the test case
              test_name = test_code.split('class ')[1].split('(')[0]
              test_cls = exec_ns[test_name]
              suite    = unittest.TestLoader().loadTestsFromTestCase(test_cls)
              result   = unittest.TextTestRunner(stream=None).run(suite)

              if result.wasSuccessful():
                  self.show_success_screen(self.quests[self.current_quest_idx])
              else:
                  display(HTML("""
                  <div class='error-message'>
                      ⚠️ Not quite there yet—review the failures below:
                  </div>
                  """))
                  for _, tb in result.failures:
                      print(tb)

          except Exception as e:
              display(HTML(f"""
              <div class='error-message'>
                  ⚠️ Your code raised an exception:
                  <pre>{str(e)}</pre>
              </div>
              """))
              print(traceback.format_exc())

    def show_hint(self, _):
        self.output_area.clear_output()
        with self.output_area:
            hints = self.quests[self.current_quest_idx].get('hints', [])
            if hints:
                display(HTML(f"""
                <div class='hint-message'>
                    💡 Hint: {hints[0]}
                </div>
                """))

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
            next_btn = widgets.Button(description='➡️ Next Quest', button_style='success')
            next_btn.on_click(lambda _: self.advance_to_next_quest())
            display(next_btn)
        else:
            display(HTML("""
            <div class="success-text">
                All quests complete! You are now a Coding Warrior! 🏆
            </div>
            """))
        display(HTML('</div>'))

    def advance_to_next_quest(self):
        self.current_quest_idx += 1
        self.output_area.clear_output()
        self.create_ui()
