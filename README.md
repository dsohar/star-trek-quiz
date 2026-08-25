# 🖖 Star Trek Quiz

- 🐳 **[Docker Hub](https://hub.docker.com/r/dsohar/star-trek-quiz)**
- 💻 **[GitHub Repository](https://github.com/dsohar/star-trek-quiz)**

## Overview

Star Trek Quiz is a Python web application built with Flask.

The application presents the player with a 10-question Star Trek: The Next Generation trivia quiz selected randomly from a larger question bank.

Each quiz contains:

- 3 easy questions worth 1 point each
- 4 medium questions worth 2 points each
- 3 hard questions worth 3 points each

The maximum possible score is 20 points.

After each answer, the player is shown whether the answer was correct and their current score. At the end of the quiz, the player can enter their name to save their score to the leaderboard or return to the home page without saving it.

The leaderboard displays the top 10 scores.

The project was originally created as a Docker exercise and demonstrates how to package and run a Python Flask web application inside a Docker container.

---

## Technologies

* Python 3.14
* Flask
* Jinja2
* JSON
* Docker

---

## Project Structure

```text
star-trek-quiz/
│
├── static/
│   └── favicon.ico
│
├── templates/
│   ├── home.html
│   ├── quiz.html
│   ├── result.html
│   ├── finish.html
│   └── leaderboard.html
│
├── app.py
├── star_trek_quiz.json
├── leaderboard.json
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### File Description

| File | Purpose |
| --- | --- |
| `app.py` | Main Flask application containing the routes and quiz logic. |
| `star_trek_quiz.json` | Stores the quiz questions, answers and point values. |
| `leaderboard.json` | Stores player names and scores. |
| `home.html` | Displays the main menu. |
| `quiz.html` | Displays the current quiz question and score. |
| `result.html` | Displays whether the selected answer was correct. |
| `finish.html` | Displays the final score and allows the player to submit a name. |
| `leaderboard.html` | Displays the top leaderboard scores. |
| `favicon.ico` | Browser tab icon for the application. |
| `Dockerfile` | Defines how to build the Docker image. |
| `requirements.txt` | Lists the Python dependencies. |
| `.dockerignore` | Excludes unnecessary files from the Docker image. |
| `.gitignore` | Excludes unnecessary local files from Git. |

---

## Running the Application With Docker

The application is available as a pre-built image on Docker Hub.

Run the latest version:

```bash
docker run --rm -p 5001:5001 dsohar/star-trek-quiz:latest
```

Then open your browser and navigate to:

```text
http://localhost:5001
```

If the image is not already available locally, Docker will automatically pull it from Docker Hub.

### Running a Specific Version

To run version 2.0.0:

```bash
docker run --rm -p 5001:5001 dsohar/star-trek-quiz:2.0.0
```

### Docker Image

Docker Hub repository:

`dsohar/star-trek-quiz`

Available application version:

`dsohar/star-trek-quiz:2.0.0`

The `latest` tag points to the current version.

> **Note:** The leaderboard is currently stored inside the container. Scores created while running the Docker image are therefore lost when the container is removed. Persistent storage will be added as part of the Kubernetes deployment.

---

## Running the Application Without Docker

### Requirements

- Python 3.14
- pip

### Clone the Repository

```bash
git clone https://github.com/dsohar/star-trek-quiz.git
cd star-trek-quiz
```

### Create a Virtual Environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the Application

```bash
python app.py
```

Open your browser and navigate to:

```text
http://localhost:5001
```

---

## Versions

### v2.0.0

- Added complete 10-question games
- Added easy, medium and hard question difficulty levels
- Added point-based scoring
- Expanded the Star Trek: The Next Generation question bank
- Added Flask session-based game state
- Added player name submission
- Added a top-10 leaderboard
- Added a home screen
- Added a browser favicon

### v1.0.0

- Initial Flask application
- Random Star Trek trivia questions
- Docker support
- Docker Hub distribution