# Development Setup

## Prerequisites

- Python 3.11+
- PostgreSQL for production-like local development
- Git

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app manage.py db upgrade
python run.py
```

The app defaults to local SQLite when `DATABASE_URL` is not provided. Use PostgreSQL locally when validating deployment behavior.

## Branching

Use `main` for production-ready code, `develop` for integration, and short-lived `feature/*`, `bugfix/*`, `hotfix/*`, or `release/*` branches.
