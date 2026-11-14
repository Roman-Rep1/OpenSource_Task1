# WSB Pizzeria

**A small Flask web application demonstrating a complete introductory workflow: relational data, a browser interface, Docker containerization, Azure Container Registry publication, and automated UI testing.**

> **Scope:** Demonstration application, not a production-ready commerce system. Checkout is simulated; orders are not persisted, payments are not processed, and authentication is not implemented.

## Overview

WSB Pizzeria lets visitors browse a seeded pizza menu, filter pizzas by name, select a pizza, add optional toppings, see a calculated cart total, and submit a simulated order. The Flask server renders the initial page using database records; browser-side JavaScript handles search and cart interactions and sends a POST request to the checkout endpoint.

## Features

- Pizza menu with descriptions and prices, loaded from SQLite.
- Case-insensitive, client-side pizza-name filtering.
- Single-pizza cart with optional toppings and a calculated total in PLN.
- Simulated checkout using `POST /order` and a JSON success response.
- Containerized local execution with Docker.
- Browser-driven UI tests using Robot Framework and SeleniumLibrary.
- Container image publication to Azure Container Registry (ACR).

## Technology stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Backend | Python 3.13, Flask 3.0.2 | HTTP routes and server-side HTML rendering |
| Persistence | SQLite, Flask-SQLAlchemy 3.1.1 | Pizza and topping models and seed data |
| Frontend | HTML, Bootstrap, JavaScript | Menu, search, cart and checkout interactions |
| Containerization | Docker, `python:3.13-slim` | Reproducible application packaging |
| Cloud registry | Microsoft Azure Container Registry | Storage and distribution of Docker images; **not** application hosting |
| UI automation | Robot Framework, SeleniumLibrary | Automated browser interaction and assertions |
| Version control | Git, GitHub | Commits, feature branches, pull requests and review |

## Architecture

```text
Browser
  | GET /                    POST /order
  v                              |
Flask application  <-------------+
  | render_template()              returns JSON success (mock)
  v
HTML + JavaScript (filter, cart, toppings)
  ^
  | pizzas and toppings
Flask-SQLAlchemy
  |
SQLite database (seeded at startup)

Dockerfile -> Docker image -> local Docker container
                         \-> Azure Container Registry (image storage)
```

Pushing an image to ACR does not deploy a running public website. A separate compute service (such as Azure Container Apps or App Service) would be needed for hosted execution.

## Repository layout

```text
.
├── app.py                     # Flask application, models and endpoints
├── templates/
│   └── index.html             # Server-rendered page and client-side interactions
├── requirements.txt           # Application Python dependencies
├── requirements-tests.txt     # Robot Framework test dependencies
├── test.robot                 # Automated pizza search UI tests
├── Dockerfile                 # Docker image build instructions
├── .dockerignore              # Exclusions from the Docker build context
├── .gitignore                 # Exclusions from Git
└── README.md
```

An optional `test_pizzeria.robot` example suite may also be present. Commit only the test suites maintained as part of the project. Generated `results/` files should normally be excluded from Git; retain them locally or publish them as CI artifacts when test results need to be inspected.

## Prerequisites

- Python 3.13 (or a compatible version for the listed dependencies)
- Docker Desktop, running with a working Docker engine
- For UI tests: a supported browser and matching Selenium/WebDriver setup
- For optional ACR publication: Azure CLI, an Azure subscription and permission to push images to an ACR instance

## Run locally without Docker

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000/` in your browser. The app creates its SQLite tables and inserts sample pizzas and toppings when the database is empty. Flask-SQLAlchemy may place the relative SQLite database under Flask's instance directory.

## Run with Docker

From the repository root:

```powershell
docker build -t wsb-pizzeria:2.0 .
docker run --rm --name wsb-pizzeria -p 5000:5000 wsb-pizzeria:2.0
```

Visit `http://127.0.0.1:5000/`. Stop the foreground container with `Ctrl+C`. If port 5000 is in use, change the host-side port (for example `-p 5001:5000`) and visit that port instead.

**Data persistence:** The sample Docker configuration does not mount a persistent volume. Data written inside the container can be lost when that container is removed. The database is seeded again when a fresh container starts.

## API reference

| Method | Path | Response | Notes |
| --- | --- | --- | --- |
| `GET` | `/` | HTML page | Queries pizzas and toppings and renders `templates/index.html` |
| `POST` | `/order` | `{"status":"success","message":"Order placed successfully!"}` | Mock endpoint; does not validate or persist an order |

Example request:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/order
```

## Automated UI tests

Install test-only dependencies:

```powershell
python -m pip install -r requirements-tests.txt
```

Start the application (locally or in Docker), then run:

```powershell
python -m robot --outputdir results test.robot
```

Robot Framework produces `results/report.html`, `results/log.html`, and `results/output.xml`. Open `results/report.html` to inspect the outcome. The `test.robot` suite checks pizza search behavior, including case-insensitive matching and an empty-result scenario. **Verify outcomes from an actual test run; the presence of test scripts alone does not demonstrate that the tests passed.**

> `test_pizzeria.robot`, if present, is a separate example suite that uses Firefox and exercises home-page and checkout interactions. `test.robot` contains the pizza-search UI tests.

## Publish an image to Azure Container Registry

Replace `<registry-name>` with your actual Azure Container Registry resource name:

```powershell
az login
az acr login --name <registry-name>
$LOGIN_SERVER = az acr show --name <registry-name> --query loginServer --output tsv
docker tag wsb-pizzeria:2.0 "$LOGIN_SERVER/wsb-pizzeria:2.0"
docker push "$LOGIN_SERVER/wsb-pizzeria:2.0"
```

Verify the pushed repository and tags in Azure Portal → Container registries → your registry → Repositories. Never commit Azure credentials, access tokens or registry passwords.

## Development workflow

The project was organized with Git commits and a dedicated `feature/pizzeria-tests` branch. The branch introduced Robot Framework tests and a subsequent text-encoding fix. Changes were reviewed through a GitHub pull request before merging into `main`.

Typical workflow:

```powershell
git switch -c feature/my-change
# edit and test
git add <changed-files>
git commit -m "feat: describe the change"
git push -u origin feature/my-change
# open PR, review diff, merge, then update local main
git switch main
git pull --ff-only origin main
```

## Limitations and next steps

This is a learning project. To move toward a production-grade application, order persistence and input validation, automated backend tests, configuration via environment variables, database migrations, persistent database storage, structured logging, a production WSGI server, CI checks, security hardening, and actual cloud hosting might be added. SQLite is adequate for this demo; PostgreSQL would be a reasonable next step for a more demanding multi-user system.

## License

No license has been specified. **Do not assume the repository is open-source licensed** until a suitable `LICENSE` file is explicitly added.
