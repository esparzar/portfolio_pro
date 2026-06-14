# Portfolio Pro

Portfolio Pro is a production-oriented personal portfolio platform built with Flask and PostgreSQL. It includes a public portfolio site, admin content management screens, contact capture, REST API endpoints, authentication, migrations, and Render-ready deployment configuration.

Live demo: https://emmanuel-amponsah.onrender.com

## Features

- Public homepage, about page, project listing, project detail pages, and contact form
- Admin dashboard for project and contact management
- Flask-Login authentication for browser admin sessions
- JWT-protected API endpoints for admin API operations
- SQLAlchemy models with Flask-Migrate migrations
- Contact persistence with optional SMTP notification
- Custom error pages for common failures
- Health endpoint at `/health` for deployment checks
- Pytest test structure with unit and integration coverage
- Ruff, Black, isort, and GitHub Actions CI preparation

## Tech Stack

- Python, Flask, SQLAlchemy, Flask-Migrate
- Flask-Login, Flask-WTF, WTForms
- Flask-RESTful, Flask-JWT-Extended, Flask-Limiter
- PostgreSQL in production, SQLite fallback for local development
- Gunicorn and Render for deployment
- pytest, pytest-flask, factory-boy

## Architecture

```text
portfolio_pro/
├── app/
│   ├── admin/
│   ├── api/
│   ├── auth/
│   ├── errors/
│   ├── forms/
│   ├── main/
│   ├── models/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── utils/
│   └── __init__.py
├── docs/
├── migrations/
├── scripts/
├── tests/
├── config.py
├── manage.py
├── run.py
├── wsgi.py
└── requirements.txt
```

The application uses the Flask application factory pattern. Feature routes are grouped into `main`, `auth`, and `admin` blueprints, while JSON endpoints are registered from `app/api`. Shared infrastructure such as logging, error handlers, template filters, and extension initialization is centralized.

## Installation

This project uses `proenv` as the official local virtual environment directory.

```bash
git clone <repository-url>
cd portfolio_pro
python -m venv proenv
source proenv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with local secrets and database settings before running production-like workflows.

## Environment Variables

Key variables:

- `FLASK_CONFIG`: `local`, `development`, `testing`, or `production`
- `SECRET_KEY`: Flask session signing secret
- `JWT_SECRET_KEY`: JWT signing secret
- `DATABASE_URL`: PostgreSQL connection URL
- `ADMIN_EMAIL`: notification recipient
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`: SMTP configuration
- `CORS_ORIGINS`: comma-separated allowed API origins
- `REDIS_URL`: optional rate-limit storage backend

See `.env.example` for a complete template.

## Database Setup

For local SQLite fallback, no PostgreSQL URL is required. For PostgreSQL, set `DATABASE_URL`, then run:

```bash
flask --app manage.py db upgrade
flask --app manage.py create-admin
```

## Running Locally

```bash
python run.py
```

The app runs at `http://localhost:5000` by default.

## Running With Docker

Copy the example environment file and adjust secrets before starting containers:

```bash
cp .env.example .env
```

For Docker, `DATABASE_URL` must use the Compose database hostname:

```text
postgresql://portfolio_user:portfolio_password@db:5432/portfolio_pro
```

Build and start the application:

```bash
docker compose config
docker compose build
docker compose up
```

Open the app at `http://127.0.0.1:5000` and check health at `http://127.0.0.1:5000/health`.

Run migrations and verification commands in the running `web` container:

```bash
docker compose exec web flask db upgrade
docker compose exec web pytest
docker compose exec web python scripts/verify_startup.py
```

Stop containers:

```bash
docker compose down
```

Reset the local Docker database volume:

```bash
docker compose down -v
docker compose up --build
```

If `web` cannot connect to PostgreSQL, confirm `.env` uses `POSTGRES_HOST=db` and a `DATABASE_URL` with `@db:5432`, not `@localhost:5432`.

## Testing

```bash
pytest
```

Quality checks:

```bash
ruff check .
black --check .
isort --check-only .
```

## Deployment

Render configuration:

- Build command: `bash build.sh`
- Start command: `gunicorn wsgi:app`
- Environment: `FLASK_CONFIG=production`
- Health check path: `/health`

Run migrations with `flask db upgrade` from a trusted deployment shell or release process.

## Screenshots

Add screenshots for:

- Homepage
- Projects page
- Project detail page
- Admin dashboard
- Contact workflow

Current static project screenshots live under `app/static/images/project/`.

## Future Improvements

- Add coverage reporting thresholds in CI
- Add API schema validation with Marshmallow or Pydantic
- Move email delivery to a background worker if traffic grows
- Add Redis-backed rate limiting in production
- Add admin audit logging for content changes
- Add browser-level smoke tests for critical public pages

## License

This project is maintained as a professional portfolio and learning resource.
