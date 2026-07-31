import json
import random
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

PROJECT_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = PROJECT_DIR / "star_trek_quiz.json"


def load_questions() -> list:
    """Load quiz questions from the JSON file."""

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def quiz():
    """Display a random quiz question."""

    questions = load_questions()
    question = random.choice(questions)

    answers = question["correct"] + question["incorrect"]
    random.shuffle(answers)

    return render_template(
        "quiz.html",
        question=question,
        answers=answers
    )


@app.route("/answer", methods=["POST"])
def check_answer():
    """Check the submitted answer."""

    selected_answer = request.form["answer"]
    correct_answer = request.form["correct_answer"]
    points = request.form["points"]

    is_correct = selected_answer == correct_answer

    return render_template(
        "result.html",
        is_correct=is_correct,
        correct_answer=correct_answer,
        points=points
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)