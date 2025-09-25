# django-sprint-tracker

A simple Agile sprint and task tracker built with Django REST Framework.  

Supports user authentication (JWT), role-based permissions, projects, sprints, tasks.

## Setup & Running Locally

### Using Docker

Steps:
1. Copy `.env.example` to `.env` and fill in DB credentials.

2. Build and start services:
   ```sh
   docker compose --profile dev up --build
   ```
3. The API will be available at http://localhost:8000.

Run tests:
```sh
docker compose --profile test up --build --abort-on-container-exit
```
### Local Python (venv)

1. Create and activate a virtual environment:
    ```sh
    python -m venv venv

    source venv/bin/activate
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements-dev.txt
    ```
3. Copy .env.example to .env and set DB credentials.
4. Apply migrations:
    ```sh
    python manage.py migrate
    ```
5. Create a superuser (optional, for admin access):
    ```sh
    python manage.py createsuperuser
    ```
6. Run the server:
    ```sh
    python manage.py runserver
    ```
7. The API will be available at http://localhost:8000.

Run tests:
```sh
pytest
```

## Linting & Formatting
To test files for any linting issues:
```sh
ruff check
```

Fix:
```sh
ruff check --fix
```
