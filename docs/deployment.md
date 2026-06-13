# Deployment

Portfolio Pro is configured for Render with Gunicorn and PostgreSQL.

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
