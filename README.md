# 🖖 Star Trek Quiz

- 🐳 **[Docker Hub](https://hub.docker.com/r/dsohar/star-trek-quiz)**
- 💻 **[GitHub Repository](https://github.com/dsohar/star-trek-quiz)**

## Overview

Star Trek Quiz is a simple Python web application built with Flask.

Each time the home page is loaded, the application displays a random Star Trek trivia question with four possible answers. After selecting an answer, the user is informed whether the answer was correct.

The project was created as a Docker exercise and demonstrates how to package and run a Python web application inside a Docker container.

---

## Technologies

* Python 3.14
* Flask
* Docker

---

## Project Structure

```text
star-trek-quiz/
│
├── templates/
│   ├── quiz.html
│   └── result.html
│
├── app.py
├── star_trek_quiz.json
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

### File Description

| File                  | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| `app.py`              | Main Flask application.                           |
| `star_trek_quiz.json` | Stores all quiz questions and answers.            |
| `quiz.html`           | Displays a quiz question.                         |
| `result.html`         | Displays whether the selected answer was correct. |
| `Dockerfile`          | Defines how to build the Docker image.            |
| `requirements.txt`    | Lists the Python dependencies.                    |
| `.dockerignore`       | Excludes unnecessary files from the Docker image. |

---

## Running the Application With Docker

Run the following command:

```bash
docker run --rm -p 5001:5001 dsohar/star-trek-quiz:latest
```

Then open your browser and navigate to:

```
http://localhost:5001
```

### Docker image

The application is available on Docker Hub as:

dsohar/star-trek-quiz:latest

---

## Running the Application Without Docker

### Create a virtual environment

macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the application

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:5001
```

---