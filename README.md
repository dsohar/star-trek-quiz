## 🖖 Star Trek Quiz

* 🐳 **Docker Hub:** https://hub.docker.com/r/dsohar/star-trek-quiz
* 💻 **GitHub Repository:** https://github.com/dsohar/star-trek-quiz
* 🚀 **GitOps Repository:** https://github.com/dsohar/GitOps

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

> **Note:** The leaderboard is a JSON file inside each container. Kubernetes Pods do not share scores, and scores can be lost when a container is replaced or removed. Shared persistent storage or a database is a possible future improvement.

---

## Technologies

* Python 3.14
* Flask
* Jinja2
* JSON
* Docker
* Kubernetes
* Helm
* Jenkins
* Trivy
* Argo CD

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
├── Jenkinsfile
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
| `Jenkinsfile`                         | Defines the Jenkins CI and GitOps publishing pipeline.                 |
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

To run a specific version, choose an existing tag from the Docker Hub repository and replace `<IMAGE_TAG>`:

```bash
docker run --rm -p 5001:5001 dsohar/star-trek-quiz:<IMAGE_TAG>
```

### Docker Image

Docker Hub repository:

`dsohar/star-trek-quiz`

Jenkins publishes a build-numbered image and also updates `latest`. Tags can be deleted or changed; check Docker Hub for available tags. Pin a versioned tag when you need a specific build.

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

The chart defaults to the `latest` image tag. This section describes a **direct Helm release**; it is separate from the Argo CD GitOps workflow below. Do not manage the same Kubernetes resources through both methods.

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

The chart constructs the host from `ingress.ip` (default `192.168.49.2`) and routes `/`. Set `--set ingress.ip=<INGRESS-IP>` on install or upgrade if needed, and ensure the NGINX ingress controller and DNS routing are available. Then open:

```text
http://star-trek-quiz.<INGRESS-IP>.nip.io/
```


### Upgrade the Application

To update a direct Helm release, run the following from the repository. To deploy a particular image, add `--set-string image.tag=<IMAGE_TAG>`. Reusing `latest` alone does not guarantee a rollout when the manifest is unchanged:

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

## Jenkins CI and GitOps Deployment

The supplied `Jenkinsfile` uses a Jenkins shared library and a Kubernetes-based agent. It checks out the application, builds a Docker image tagged `2.2.<BUILD_NUMBER>`, scans the image with Trivy for HIGH and CRITICAL vulnerabilities, and pushes both the versioned tag and `latest` to Docker Hub. Trivy uses exit code 0, so reported vulnerabilities do not fail the pipeline. The Trivy and SonarQube stages run in parallel. The SonarQube stage currently only prints a message; its scan commands remain commented out.

Jenkins then renders `./helmchart` with `helm template` and commits the generated `star-trek-quiz-template.yaml` to the [GitOps repository](https://github.com/dsohar/GitOps) when it changes. The pipeline passes the build-numbered image tag to Helm, so the generated manifest specifies that build. After Jenkins commits the updated manifest, manually sync the Argo CD application and verify the deployment.

### Manual Argo CD sync

1. Confirm that the desired manifest and image tag are committed to the GitOps repository's `main` branch. The supplied Argo CD Application points to the repository root and the `default` namespace.
2. In the Argo CD UI, refresh the `star-trek-quiz` application and review the differences.
3. Select **Sync**, confirm the operation, and check that the application and its resources become healthy. Verify the running image and tag in the Deployment or Pods.

A sync applies the desired manifest; it does not make a mutable `latest` tag identify a particular build. Direct `helm install`, `helm upgrade`, and `helm rollback` operate on a Helm release and are not the GitOps deployment or rollback procedure. For GitOps rollback, restore the desired manifest in Git and manually sync it in Argo CD.

### Course project limitations

* **Leaderboard:** Each Pod writes its own local JSON file; scores are neither shared nor durable across container replacement.
* **Flask secret:** The chart's `replace-me` value is a demo placeholder. The generated GitOps manifest includes it as Kubernetes Secret `stringData`; use an appropriate secret-management approach for a real deployment and do not commit real keys.
* **Trivy:** The scan reports HIGH and CRITICAL findings but does not fail the pipeline on vulnerabilities.
* **Ingress:** The host pattern and default IP are specific to the exercise. The IP is configurable in Helm values, but the hostname pattern is hardcoded in the template and must suit the cluster's routing.

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
