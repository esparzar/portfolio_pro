# Coding Standards

## Python

- Format with Black.
- Sort imports with isort.
- Lint with Ruff.
- Keep route handlers thin and move side effects into services when they grow.
- Keep models focused on persistence, query helpers, and serialization.

## Flask

- Register new page routes in the relevant feature blueprint.
- Register new JSON endpoints through `app/api/__init__.py`.
- Keep environment-specific settings in `config.py`.
- Never hardcode secrets or production credentials.

## Security

- Use CSRF-protected WTForms for browser forms.
- Use Flask-Login for admin web sessions.
- Use JWT only for API clients.
- Avoid logging secrets, passwords, tokens, or full credential payloads.
