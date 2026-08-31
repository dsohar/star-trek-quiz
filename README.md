## 🖖 Star Trek Quiz

* 🐳 **Docker Hub:** https://hub.docker.com/r/dsohar/star-trek-quiz
* 💻 **GitHub Repository:** https://github.com/dsohar/star-trek-quiz

## Overview

Star Trek Quiz is a Python web application built with Flask.

The application presents the player with a 10-question Star Trek: The Next Generation trivia quiz selected randomly from a larger question bank.

Each quiz contains:

* 3 easy questions worth 1 point each
* 4 medium questions worth 2 points each
* 3 hard questions worth 3 points each

The maximum possible score is 20 points.

After each answer, the player is shown whether the answer was correct and their current score. At the end of the quiz, the player can enter their name to save their score to the leaderboard or return to the home page without saving it.

The leaderboard displays the top 10 scores.

> **Note:** The leaderboard is currently stored inside the container. Scores created while running the Docker image are therefore lost when the container is removed. Persistent storage will be added at a later stage.

---

## Technologies

* Python 3.14
* Flask
* Jinja2
* JSON
* Docker
* Kubernetes
* Helm

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
├── helmchart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── NOTES.txt
│       ├── _helpers.tpl
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── ingress.yaml
│       ├── secret.yaml
│       └── service.yaml
│
├── app.py
├── star-trek-quiz.json
├── leaderboard.json
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### File Description

| File                                  | Purpose                                                          |
| ------------------------------------- | ---------------------------------------------------------------- |
| `app.py`                              | Main Flask application containing the routes and quiz logic.     |
| `star-trek-quiz.json`                 | Stores the quiz questions, answers and point values.             |
| `leaderboard.json`                    | Stores player names and scores.                                  |
| `templates/home.html`                 | Displays the main menu.                                          |
| `templates/quiz.html`                 | Displays the current quiz question and score.                    |
| `templates/result.html`               | Displays whether the selected answer was correct.                |
| `templates/finish.html`               | Displays the final score and allows the player to submit a name. |
| `templates/leaderboard.html`          | Displays the top leaderboard scores.                             |
| `static/favicon.ico`                  | Browser tab icon for the application.                            |
| `Dockerfile`                          | Defines how to build the Docker image.                           |
| `Jenkinsfile`                         | Defines a Jenkins pipeline that builds a Docker.                 |
| `requirements.txt`                    | Lists the Python dependencies.                                   |
| `.dockerignore`                       | Excludes unnecessary files from the Docker image.                |
| `.gitignore`                          | Excludes unnecessary local files from Git.                       |
| `helmchart/.helmignore`               | Excludes unnecessary local files from Helm.                      |
| `helmchart/Chart.yaml`                | Defines the Helm chart metadata.                                 |
| `helmchart/values.yaml`               | Contains configurable values used by the Helm chart.             |
| `helmchart/templates/deployment.yaml` | Defines the Kubernetes Deployment and application Pods.          |
| `helmchart/templates/service.yaml`    | Defines the Kubernetes Service.                                  |
| `helmchart/templates/ingress.yaml`    | Defines the NGINX Ingress.                                       |
| `helmchart/templates/configmap.yaml`  | Creates the ConfigMap used for application configuration.        |
| `helmchart/templates/secret.yaml`     | Creates the Kubernetes Secret used for the Flask secret key.     |
| `helmchart/templates/_helpers.tpl`    | Contains reusable Helm template labels.                          |
| `helmchart/templates/NOTES.txt`       | Displays information after a Helm install or upgrade.            |

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

To run a specific version, replace the tag with the required version. For example:

```bash
docker run --rm -p 5001:5001 dsohar/star-trek-quiz:2.1.0
```

### Docker Image

Docker Hub repository:

`dsohar/star-trek-quiz`

The `latest` tag points to the current version.

---

## Running the Application With Kubernetes and Helm

The Helm chart deploys the application to Kubernetes using the Docker image from Docker Hub.

The deployment includes:
* 3 application replicas
* A ClusterIP Service
* An NGINX Ingress
* A ConfigMap
* A Kubernetes Secret
* Liveness and readiness probes
* CPU and memory resource requests and limits
* Pod anti-affinity to prefer distributing replicas across different Kubernetes nodes.

The Docker image can be pulled using the `latest` tag.

### Install the Application

```bash
helm install enterprise ./helmchart \
  --set-string secret.secretKey="your-secret-key"
```

Check the deployed resources:

```bash
kubectl get pods
kubectl get service
kubectl get ingress
```

Then open your browser and navigate to:

```text
http://<INGRESS-ADDRESS>/star-trek-quiz
```


### Upgrade the Application

After a new Docker image has been built and pushed to Docker Hub:

```bash
helm upgrade enterprise ./helmchart \
  --set-string secret.secretKey="your-secret-key"
```

### Roll Back

To roll back to a previous Helm revision:

```bash
helm rollback enterprise <revision>
```

---

## Running the Application Locally

### Requirements

* Python 3.14
* pip

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

### v2.1.0

* Added Kubernetes deployment using Helm
* Added Deployment, Service and Ingress resources
* Added ConfigMap and Kubernetes Secret
* Added liveness and readiness health checks
* Added CPU and memory resource requests and limits
* Added pod anti-affinity for distributing replicas across Kubernetes nodes
* Added Helm upgrade and rollback support

### v2.0.0

* Added complete 10-question games
* Added easy, medium and hard question difficulty levels
* Added point-based scoring
* Expanded the Star Trek: The Next Generation question bank
* Added Flask session-based game state
* Added player name submission
* Added a top-10 leaderboard
* Added a home screen
* Added a browser favicon

### v1.0.0

* Initial Flask application
* Random Star Trek trivia questions
* Docker support
* Docker Hub distribution
