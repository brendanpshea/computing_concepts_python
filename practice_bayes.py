# practice_bayes.py
import random
from typing import Dict, List, Tuple
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd

class BayesTheorem:
    def __init__(self):
        # Each problem type has its own complete template
        self.problems = {
            "medical": {
                "template": (
                    "A medical test is being used to detect a rare condition. "
                    "Studies show that {prob_h}% of people have this condition. "
                    "When someone has the condition, the test comes back positive {prob_e_given_h}% of the time. "
                    "When someone doesn't have the condition, the test comes back positive {prob_e_given_not_h}% of the time."
                    "<br><br><b>Question: If a person tests positive, what is the probability "
                    "they actually have the condition? [Calculate P(H|E)]</b>"
                ),
                "H": "having the condition",
                "E": "testing positive",
                "wrong_h": "getting a positive test result"
            },
            "security": {
                "template": (
                    "A company is evaluating their security system. "
                    "Historical data shows that {prob_h}% of nights have actual break-in attempts. "
                    "When there is a break-in, the alarm triggers {prob_e_given_h}% of the time. "
                    "On nights with no break-in, false alarms occur {prob_e_given_not_h}% of the time."
                    "<br><br><b>Question: If the alarm goes off, what is the probability "
                    "there is actually a break-in? [Calculate P(H|E)]</b>"
                ),
                "H": "break-in occurring",
                "E": "alarm triggering",
                "wrong_h": "alarm going off"
            },
            "spam": {
                "template": (
                    "An email service analyzes its spam detection system. "
                    "Their data shows that {prob_h}% of incoming emails are spam. "
                    "The filter correctly identifies {prob_e_given_h}% of spam emails. "
                    "However, it incorrectly flags {prob_e_given_not_h}% of legitimate emails as spam."
                    "<br><br><b>Question: If an email is flagged as spam, what is the probability "
                    "it is actually spam? [Calculate P(H|E)]</b>"
                ),
                "H": "email being spam",
                "E": "being flagged as spam",
                "wrong_h": "being marked by the filter"
            },
            "drug_test": {
        "template": (
            "A company conducts random drug testing on employees. "
            "Based on previous studies, {prob_h}% of employees use banned substances. "
            "The drug test correctly identifies {prob_e_given_h}% of actual users. "
            "However, it also shows positive for {prob_e_given_not_h}% of non-users due to chemical similarities with legal substances."
            "<br><br><b>Question: If an employee tests positive, what is the probability "
            "they actually use banned substances? [Calculate P(H|E)]</b>"
        ),
        "H": "using banned substances",
        "E": "testing positive",
        "wrong_h": "getting a positive drug test"
    },

    "weather": {
        "template": (
            "A weather app predicts rain based on cloud patterns. "
            "In this region, it rains on {prob_h}% of days. "
            "When it does rain, the app predicted it correctly {prob_e_given_h}% of the time. "
            "However, the app also predicts rain on {prob_e_given_not_h}% of days that end up being dry."
            "<br><br><b>Question: If the app predicts rain tomorrow, what is the probability "
            "it will actually rain? [Calculate P(H|E)]</b>"
        ),
        "H": "raining tomorrow",
        "E": "app predicting rain",
        "wrong_h": "app showing rain prediction"
    },

    "quality_control": {
        "template": (
            "A factory uses an automated system to detect defective products. "
            "Typically, {prob_h}% of products have defects. "
            "The system successfully identifies {prob_e_given_h}% of actually defective items. "
            "However, it incorrectly flags {prob_e_given_not_h}% of good products as defective."
            "<br><br><b>Question: If the system flags a product as defective, what is the probability "
            "it actually has a defect? [Calculate P(H|E)]</b>"
        ),
        "H": "product being defective",
        "E": "system flagging as defective",
        "wrong_h": "getting flagged by the system"
    },

    "college": {
        "template": (
            "A college uses a predictive model to identify students at risk of dropping out. "
            "Historical data shows {prob_h}% of students eventually drop out. "
            "The model correctly identifies {prob_e_given_h}% of students who do drop out. "
            "However, it falsely flags {prob_e_given_not_h}% of graduating students as at-risk."
            "<br><br><b>Question: If the model flags a student as at-risk, what is the probability "
            "they will actually drop out? [Calculate P(H|E)]</b>"
        ),
        "H": "student dropping out",
        "E": "being flagged as at-risk",
        "wrong_h": "getting flagged by the model"
    },

    "fraud": {
        "template": (
            "A bank's AI system monitors transactions for fraud. "
            "Analysis shows that {prob_h}% of transactions are fraudulent. "
            "The system detects {prob_e_given_h}% of actual fraud attempts. "
            "However, it also flags {prob_e_given_not_h}% of legitimate transactions as suspicious."
            "<br><br><b>Question: If a transaction is flagged as suspicious, what is the probability "
            "it is actually fraudulent? [Calculate P(H|E)]</b>"
        ),
        "H": "transaction being fraudulent",
        "E": "being flagged as suspicious",
        "wrong_h": "getting flagged by the system"
    },

    "admission": {
        "template": (
            "A university study examines the predictive power of high SAT scores. "
            "Among all applicants, {prob_h}% become successful students (GPA > 3.5). "
            "Among successful students, {prob_e_given_h}% had high SAT scores. "
            "However, {prob_e_given_not_h}% of students who struggle also had high SAT scores."
            "<br><br><b>Question: If an applicant has high SAT scores, what is the probability "
            "they will be successful? [Calculate P(H|E)]</b>"
        ),
        "H": "being a successful student",
        "E": "having high SAT scores",
        "wrong_h": "scoring high on the SAT"
    },

    "disease_spread": {
        "template": (
            "An epidemiologist studies a new infection using a rapid test. "
            "In the current population, {prob_h}% of people are infected. "
            "The rapid test detects {prob_e_given_h}% of actual infections. "
            "However, it shows positive for {prob_e_given_not_h}% of healthy individuals."
            "<br><br><b>Question: If someone tests positive on the rapid test, what is the probability "
            "they are actually infected? [Calculate P(H|E)]</b>"
        ),
        "H": "being infected",
        "E": "testing positive",
        "wrong_h": "getting a positive test result"
    },
            "simulation": {
        "template": (
            "A philosopher considers the simulation hypothesis. "
            "Given current technological trends, they estimate a {prob_h}% chance we live in a simulation. "
            "If we are in a simulation, they argue we would see quantum physics behaving the way it does {prob_e_given_h}% of the time. "
            "However, they calculate these quantum behaviors would occur in {prob_e_given_not_h}% of non-simulated realities too."
            "<br><br><b>Question: Given our observed quantum behaviors, what is the probability "
            "we live in a simulation? [Calculate P(H|E)]</b>"
        ),
        "H": "living in a simulation",
        "E": "observing our quantum behaviors",
        "wrong_h": "seeing quantum effects"
    },

    "alien_life": {
        "template": (
            "SETI researchers analyze a potential alien signal. "
            "Based on Drake equation estimates, they calculate a {prob_h}% probability of advanced civilizations existing within range. "
            "If such civilizations exist, they would produce this type of signal {prob_e_given_h}% of the time. "
            "Natural phenomena create similar signals with probability {prob_e_given_not_h}%."
            "<br><br><b>Question: Given the detected signal, what is the probability "
            "it comes from an alien civilization? [Calculate P(H|E)]</b>"
        ),
        "H": "signal being from aliens",
        "E": "detecting this type of signal",
        "wrong_h": "receiving an unusual signal"
    },

    "ai_consciousness": {
        "template": (
            "An AI researcher studies machine consciousness. "
            "They estimate that {prob_h}% of information processing systems are conscious. "
            "A conscious system would pass their new awareness test {prob_e_given_h}% of the time. "
            "However, they find that {prob_e_given_not_h}% of definitely non-conscious systems also pass it."
            "<br><br><b>Question: If an AI system passes the awareness test, what is the probability "
            "it is actually conscious? [Calculate P(H|E)]</b>"
        ),
        "H": "system being conscious",
        "E": "passing the awareness test",
        "wrong_h": "showing test-passing behavior"
    },

    "multiverse": {
        "template": (
            "A cosmologist evaluates the multiverse theory. "
            "Their model suggests a {prob_h}% prior probability of multiple universes existing. "
            "If the multiverse exists, we would observe our universal constants having their specific values in {prob_e_given_h}% of cases. "
            "With a single universe, these constants would arise by chance {prob_e_given_not_h}% of the time."
            "<br><br><b>Question: Given our universal constants, what is the probability "
            "the multiverse exists? [Calculate P(H|E)]</b>"
        ),
        "H": "multiverse existing",
        "E": "observing our universal constants",
        "wrong_h": "seeing these physical constants"
    },

    "historical_event": {
        "template": (
            "A historian analyzes a controversial historical document. "
            "Their prior research suggests a {prob_h}% chance the document is authentic. "
            "If authentic, it would contain certain linguistic patterns with probability {prob_e_given_h}%. "
            "They find that {1-prob_e_given_not_h}% of forgeries lack these patterns."
            "<br><br><b>Question: Given the observed linguistic patterns, what is the probability "
            "the document is authentic? [Calculate P(H|E)]</b>"
        ),
        "H": "document being authentic",
        "E": "containing these linguistic patterns",
        "wrong_h": "showing these writing patterns"
    },

    "prophecy": {
        "template": (
            "A skeptic investigates supposed prophetic dreams. "
            "In their study, {prob_h}% of reported predictions are actually made before events. "
            "When predictions are genuine, they match future events {prob_e_given_h}% of the time by actual foresight. "
            "Due to coincidence and confirmation bias, {1-prob_e_given_not_h}% of post-hoc 'predictions' fail to match events."
            "<br><br><b>Question: If a prediction matches events, what is the probability "
            "it was genuinely prophetic? [Calculate P(H|E)]</b>"
        ),
        "H": "prediction being genuine",
        "E": "matching actual events",
        "wrong_h": "seeing events match the prediction"
    },

    "ai_hallucination": {
        "template": (
            "An AI safety researcher studies large language model outputs. "
            "Analysis shows that {prob_h}% of model statements are hallucinations. "
            "When hallucinating, the model uses certain linguistic patterns {prob_e_given_h}% of the time. "
            "The model also uses these patterns in {1-prob_e_given_not_h}% of factual statements."
            "<br><br><b>Question: If the model uses these patterns, what is the probability "
            "it is hallucinating? [Calculate P(H|E)]</b>"
        ),
        "H": "model hallucinating",
        "E": "using these linguistic patterns",
        "wrong_h": "showing these language patterns"
    }
        }

    def generate_probabilities(self) -> Tuple[float, float, float]:
        """Generate random probabilities for the problem."""
        prob_h = round(random.uniform(0.1, 0.5), 2)
        prob_e_given_h = round(random.uniform(0.7, 0.95), 2)
        prob_e_given_not_h = round(random.uniform(0.05, 0.3), 2)
        return prob_h, prob_e_given_h, prob_e_given_not_h

    def format_problem(self, problem_key: str) -> Dict:
        """Format a problem with random probabilities."""
        prob_h, prob_e_given_h, prob_e_given_not_h = self.generate_probabilities()

        prob_h_percent = prob_h * 100
        prob_e_given_h_percent = prob_e_given_h * 100
        prob_e_given_not_h_percent = prob_e_given_not_h * 100

        problem_text = self.problems[problem_key]["template"].format(
            prob_h=round(prob_h_percent, 2),
            prob_e_given_h=round(prob_e_given_h_percent, 2),
            prob_e_given_not_h=round(prob_e_given_not_h_percent, 2)
        )

        return {
            "text": problem_text,
            "H": self.problems[problem_key]["H"],
            "wrong_h": self.problems[problem_key]["wrong_h"],
            "E": self.problems[problem_key]["E"],
            "prob_h": prob_h,
            "prob_e_given_h": prob_e_given_h,
            "prob_e_given_not_h": prob_e_given_not_h
        }

    def calculate_bayes(self, prob_h: float, prob_e_given_h: float, prob_e_given_not_h: float) -> float:
        """Calculate posterior probability using Bayes' Theorem."""
        prob_not_h = round(1 - prob_h, 2)
        prob_e = round((prob_e_given_h * prob_h) + (prob_e_given_not_h * prob_not_h), 2)
        prob_h_given_e = round((prob_e_given_h * prob_h) / prob_e, 2)
        return prob_h_given_e

    def show_calculation_steps(self, prob_h: float, prob_e_given_h: float, prob_e_given_not_h: float) -> pd.DataFrame:
        """Create a DataFrame showing calculation steps."""
        prob_not_h = round(1 - prob_h, 2)
        prob_e = round((prob_e_given_h * prob_h) + (prob_e_given_not_h * prob_not_h), 2)
        prob_h_given_e = round((prob_e_given_h * prob_h) / prob_e, 2)

        steps = pd.DataFrame({
            'Step': [
                'Prior probability P(H)',
                'Probability of not H: P(¬H) = 1 - P(H)',
                'Likelihood P(E|H)',
                'False positive rate P(E|¬H)',
                'Total probability P(E) = P(E|H)P(H) + P(E|¬H)P(¬H)',
                "Bayes' Theorem: P(H|E) = [P(E|H) × P(H)] / P(E)"
            ],
            'Value': [
                f'{prob_h}',
                f'{prob_not_h}',
                f'{prob_e_given_h}',
                f'{prob_e_given_not_h}',
                f'{prob_e}',
                f'{prob_h_given_e}'
            ]
        })

        return steps

class BayesWidget:
    def __init__(self):
        self.bayes = BayesTheorem()
        self.problem = None
        self.setup_widgets()

    def setup_widgets(self):
        # Basic widgets
        self.problem_text = widgets.HTML()

        # Buttons need to be initialized early
        self.check_hypothesis_btn = widgets.Button(description='Check Hypothesis')
        self.check_probs_btn = widgets.Button(description='Check Probabilities')
        self.new_problem_btn = widgets.Button(description='New Problem')

        # Output areas
        self.output = widgets.Output()
        self.feedback = widgets.HTML()

        # Button callbacks
        self.check_hypothesis_btn.on_click(self.check_hypothesis)
        self.check_probs_btn.on_click(self.check_probabilities)
        self.new_problem_btn.on_click(self.generate_new_problem)

        # Hypothesis selection
        self.hypothesis_radio = widgets.RadioButtons(
            options=[],
            description='Select the hypothesis:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='auto', margin='10px 0')
        )

        # Initial guess slider
        self.guess_slider = widgets.FloatSlider(
            value=0.5,
            min=0,
            max=1,
            step=0.01,
            description='Your initial guess for P(H|E):',
            style={'description_width': 'initial'}
        )

        # Enhanced probability inputs with descriptions
        self.prob_h_container = widgets.HBox([
            widgets.HTML(
                value="<div style='width: 400px;'>What is the base rate P(H)? <br><small>This is the general probability of the hypothesis being true, before considering evidence.</small></div>"
            ),
            widgets.FloatText(
                value=0.0,
                description='P(H):',
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='150px')
            )
        ], layout=widgets.Layout(margin='10px 0'))

        self.prob_e_given_h_container = widgets.HBox([
            widgets.HTML(
                value="<div style='width: 400px;'>What is the likelihood P(E|H)? <br><small>This is the probability of seeing the evidence when the hypothesis is true.</small></div>"
            ),
            widgets.FloatText(
                value=0.0,
                description='P(E|H):',
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='150px')
            )
        ], layout=widgets.Layout(margin='10px 0'))

        self.prob_e_given_not_h_container = widgets.HBox([
            widgets.HTML(
                value="<div style='width: 400px;'>What is the false positive rate P(E|¬H)? <br><small>This is the probability of seeing the evidence when the hypothesis is false.</small></div>"
            ),
            widgets.FloatText(
                value=0.0,
                description='P(E|¬H):',
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='150px')
            )
        ], layout=widgets.Layout(margin='10px 0'))

        # Store references to the input widgets
        self.prob_h_input = self.prob_h_container.children[1]
        self.prob_e_given_h_input = self.prob_e_given_h_container.children[1]
        self.prob_e_given_not_h_input = self.prob_e_given_not_h_container.children[1]

        # Section headers with improved styling
        self.prob_header = widgets.HTML(
            value="""
            <div style='margin: 20px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'>
                <b>Enter the Probabilities:</b>
                <br><small>Use decimals between 0 and 1 (e.g., 0.25 for 25%)</small>
            </div>
            """
        )

        self.hypothesis_header = widgets.HTML(
            value="""
            <div style='margin: 20px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'>
                <b>Identify the Hypothesis (H):</b>
                <br><small>Select the statement that represents what we're trying to find the probability of</small>
            </div>
            """
        )

        # Rest of the setup remains the same...

    def display_widget(self):
        """Display the complete widget interface."""
        title = widgets.HTML("<h2>Bayes' Theorem Practice</h2>")

        # Organize all widgets in a VBox with the new probability containers
        main_container = widgets.VBox([
            title,
            self.new_problem_btn,
            self.problem_text,
            self.hypothesis_header,
            self.hypothesis_radio,
            self.check_hypothesis_btn,
            self.guess_slider,
            self.prob_header,
            self.prob_h_container,
            self.prob_e_given_h_container,
            self.prob_e_given_not_h_container,
            self.check_probs_btn,
            self.feedback,
            self.output
        ])

        display(main_container)

        # Generate first problem
        self.generate_new_problem(None)

    def generate_new_problem(self, _):
        # Previous implementation remains the same, but update references to the new input widgets
        with self.output:
            clear_output()

        self.feedback.value = ""
        problem_key = random.choice(list(self.bayes.problems.keys()))
        self.problem = self.bayes.format_problem(problem_key)

        self.problem_text.value = f"""
            <div style='background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                {self.problem['text']}
            </div>
        """

        options = [
            (self.problem['H'], 'correct'),
            (self.problem['wrong_h'], 'wrong')
        ]
        random.shuffle(options)

        self.hypothesis_radio.options = [(desc, val) for desc, val in options]
        self.hypothesis_radio.value = None

        # Reset inputs
        self.guess_slider.value = 0.5
        self.prob_h_input.value = 0.0
        self.prob_e_given_h_input.value = 0.0
        self.prob_e_given_not_h_input.value = 0.0

    def check_hypothesis(self, _):
        """Check if the selected hypothesis is correct."""
        if self.hypothesis_radio.value == 'correct':
            self.feedback.value = """
                <div style='color: green; padding: 10px; background-color: #f0fff0; border-radius: 5px;'>
                    ✔️ Correct! This is the hypothesis (H) we're trying to determine the probability of.
                    <br>Now enter your initial guess and the probabilities.
                </div>
            """
        else:
            self.feedback.value = """
                <div style='color: red; padding: 10px; background-color: #fff0f0; border-radius: 5px;'>
                    ❌ Incorrect. Remember, the hypothesis (H) is what we're trying to determine
                    the probability of, given the evidence (E).
                </div>
            """

    def check_probabilities(self, _):
        """Check if the entered probabilities are correct."""
        with self.output:
            clear_output()

            user_probs = {
                'P(H)': round(self.prob_h_input.value, 2),
                'P(E|H)': round(self.prob_e_given_h_input.value, 2),
                'P(E|¬H)': round(self.prob_e_given_not_h_input.value, 2)
            }

            correct_probs = {
                'P(H)': round(self.problem['prob_h'], 2),
                'P(E|H)': round(self.problem['prob_e_given_h'], 2),
                'P(E|¬H)': round(self.problem['prob_e_given_not_h'], 2)
            }

            if all(abs(user_probs[k] - correct_probs[k]) < 0.01 for k in user_probs):
                # Show calculation steps
                steps_df = self.bayes.show_calculation_steps(
                    self.problem['prob_h'],
                    self.problem['prob_e_given_h'],
                    self.problem['prob_e_given_not_h']
                )

                actual = self.bayes.calculate_bayes(
                    self.problem['prob_h'],
                    self.problem['prob_e_given_h'],
                    self.problem['prob_e_given_not_h']
                )

                display(HTML("<div style='color: green; padding: 10px;'>✔️ Correct probabilities!</div>"))
                display(HTML("<h3>Calculation Steps:</h3>"))
                display(steps_df.style.set_properties(**{'text-align': 'left'}))

                display(HTML(f"""
                <div style='background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                    <h4>Results:</h4>
                    <p>Your initial guess: {round(self.guess_slider.value, 2)}</p>
                    <p>Actual P(H|E): {actual}</p>
                    <p>Difference: {abs(round(self.guess_slider.value - actual, 2))}</p>
                </div>
                """))
            else:
                display(HTML("<div style='color: red; padding: 10px;'>❌ One or more probabilities are incorrect. Try again!</div>"))

def start_practice():
    """Initialize and display the practice widget."""
    widget = BayesWidget()
    widget.display_widget()
