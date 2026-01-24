# To-Do App

A Django-based task tracker with normal and continuous tasks, dice-roll focus helper, and user authentication.

## Features
- User registration, login, logout
- Create and edit normal or continuous tasks
- Status buckets: not started, on-going, completed
- Dice roll helper: 25% break, 75% pick a random incomplete task
- Increment work time for continuous tasks

## Tech Stack
- Python 3.13
- Django (via Pipfile)
- SQLite (default dev DB)

## Prerequisites
- Python 3.10+ (3.13 recommended)
- pipenv (`pip install pipenv`)

## Setup
```bash
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Running Tests
```bash
python manage.py test
```

## Static Files
- App CSS lives at `tasks/static/tasks/style.css`
- Base template loads it via `{% load static %}` and `<link rel="stylesheet" href="{% static 'tasks/style.css' %}">`

## Project Layout
- `config/` – Django project settings and URLs
- `tasks/` – app code (models, views, forms, templates, static)
- `tasks/templates/tasks/` – HTML templates (dashboard, auth, edit)
- `tasks/static/tasks/` – CSS assets
- `db.sqlite3` – default local database

## Common Commands
- Start dev server: `python manage.py runserver`
- Create superuser: `python manage.py createsuperuser`
- Make migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## Dice Roll Behavior
- Rolls 1-4; on 1 or no incomplete tasks, you get a break.
- Otherwise assigns a random incomplete task (normal or continuous).

## Notes
- For production, configure `ALLOWED_HOSTS`, a real database, and static file hosting.