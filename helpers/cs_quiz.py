import csv
import requests

def read_questions(url):
    response = requests.get(url)
    lines = response.text.strip().split('\n')
    reader = csv.reader(lines)
    questions = [(row[0], row[1].lower()) for row in reader if len(row) == 2]
    return questions

def ask_question(question):
    user_answer = input(f"{question} (True/False): ")
    return user_answer.lower()

def cs_quiz(url):
    questions = read_questions(url)
    num_questions = len(questions)
    score = 0

    for i, (question, answer) in enumerate(questions, 1):
        print(f"\nQuestion {i} of {num_questions}:")
        user_answer = ask_question(question)
        if user_answer == answer:
            score += 1

    print(f"\nYour score: {score}/{num_questions}")

# Example usage
csv_url = "https://example.com/questions.csv"
cs_quiz(csv_url)
