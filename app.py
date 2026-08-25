import json
import random
from pathlib import Path

from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "star-trek-quiz-secret-key"

PROJECT_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = PROJECT_DIR / "star_trek_quiz.json"
LEADERBOARD_FILE = PROJECT_DIR / "leaderboard.json"


def load_questions() -> list:
    """Load quiz questions from the JSON file."""

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_leaderboard() -> list:
    """Load leaderboard entries from the JSON file."""

    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_leaderboard(leaderboard: list):
    """Save leaderboard entries to the JSON file."""

    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(leaderboard, file, indent=4)


def select_quiz_questions(questions: list) -> list:
    """Select 3 easy, 4 medium and 3 hard questions."""

    easy_questions = []
    medium_questions = []
    hard_questions = []

    for index, question in enumerate(questions):
        if question["points"] == 1:
            easy_questions.append(index)

        elif question["points"] == 2:
            medium_questions.append(index)

        elif question["points"] == 3:
            hard_questions.append(index)

    selected_questions = (
        random.sample(easy_questions, 3)
        + random.sample(medium_questions, 4)
        + random.sample(hard_questions, 3)
    )

    random.shuffle(selected_questions)

    return selected_questions


@app.route("/")
def home():
    """Display the home page."""
    return render_template("home.html")


@app.route("/start")
def start_quiz():
    """Start a new 10-question quiz."""

    questions = load_questions()

    session["questions"] = select_quiz_questions(questions)
    session["question_number"] = 0
    session["score"] = 0

    return redirect("/quiz")


@app.route("/quiz")
def quiz():
    """Display the current quiz question."""

    if "questions" not in session:
        return redirect("/")

    questions = load_questions()

    question_number = session["question_number"]
    question_index = session["questions"][question_number]

    question = questions[question_index]

    answers = question["correct"] + question["incorrect"]
    random.shuffle(answers)

    return render_template(
        "quiz.html",
        question=question,
        answers=answers,
        question_number=question_number + 1,
        score=session["score"]
    )


@app.route("/answer", methods=["POST"])
def check_answer():
    """Check the submitted answer and update the score."""

    if "questions" not in session:
        return redirect("/")

    questions = load_questions()

    question_number = session["question_number"]
    question_index = session["questions"][question_number]
    question = questions[question_index]

    selected_answer = request.form["answer"]
    correct_answer = question["correct"][0]

    is_correct = selected_answer == correct_answer

    if is_correct:
        session["score"] += question["points"]

    session["question_number"] += 1

    quiz_finished = session["question_number"] >= 10

    return render_template(
        "result.html",
        is_correct=is_correct,
        correct_answer=correct_answer,
        points=question["points"],
        score=session["score"],
        quiz_finished=quiz_finished
    )


@app.route("/finish")
def finish():
    """Display the final score and ask for a leaderboard name."""

    if "score" not in session:
        return redirect("/")

    return render_template(
        "finish.html",
        score=session["score"]
    )


@app.route("/save-score", methods=["POST"])
def save_score():
    """Save the player's score to the leaderboard."""

    if "score" not in session:
        return redirect("/")

    name = request.form["name"].strip()

    if name == "":
        return redirect("/finish")

    leaderboard = load_leaderboard()

    leaderboard.append(
        {
            "name": name,
            "score": session["score"]
        }
    )

    leaderboard.sort(
        key=lambda entry: entry["score"],
        reverse=True
    )

    save_leaderboard(leaderboard)

    return redirect("/leaderboard")


@app.route("/leaderboard")
def leaderboard():
    """Display the leaderboard."""

    leaderboard = load_leaderboard()

    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard[:10]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)