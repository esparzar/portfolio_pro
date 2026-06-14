# Deployment

Portfolio Pro is configured for Render with Gunicorn and PostgreSQL.

## Docker

The Docker setup runs the existing Flask application through Gunicorn using `wsgi:app`. It includes two services:

- `web`: builds the Flask application image, loads `.env`, waits for PostgreSQL, and exposes port `5000`.
- `db`: runs the official PostgreSQL image with a persistent `postgres_data` volume.

Redis is not included because the current application only uses Redis optionally for rate-limit storage and defaults to `memory://`.

Prepare the environment:

```bash
cp .env.example .env
```

For Docker, keep database settings aligned:

```text
POSTGRES_DB=portfolio_pro
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=portfolio_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://portfolio_user:portfolio_password@db:5432/portfolio_pro
```

Build and start:

```bash
docker compose config
docker compose build
docker compose up
```

The app is available at `http://127.0.0.1:5000`. The health endpoint is `http://127.0.0.1:5000/health`.

Run operational commands:

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

Troubleshooting:

- If PostgreSQL authentication fails, make sure `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `DATABASE_URL` agree.
- If the web container waits for PostgreSQL and exits, confirm the `db` service is healthy with `docker compose ps`.
- If migrations fail because a local volume has old credentials or schema state, reset the development volume with `docker compose down -v`.
- If `flask db upgrade` cannot find the app, confirm `FLASK_APP=wsgi:app` is present in `.env`.

## Render Settings

- Build command: `bash build.sh`
- Start command: `gunicorn wsgi:app`
- Health endpoint: `/health`

## Required Environment Variables

- `FLASK_CONFIG=production`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `ADMIN_EMAIL`

Optional email and CORS settings are listed in `.env.example`.

## Database

Run migrations during deployment or from a trusted shell:

```bash
flask db upgrade
```

Create the admin account through the Flask CLI rather than hardcoding credentials:

```bash
flask --app manage.py create-admin
```
