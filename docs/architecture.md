# Architecture

Portfolio Pro is a Flask application organized around an application factory, blueprints, extension initialization, service modules, and SQLAlchemy models.

## Runtime Flow

1. `wsgi.py` imports `create_app()` for Gunicorn and Render.
2. `app/__init__.py` loads configuration, initializes extensions, registers blueprints, attaches API resources, registers error handlers, and template filters.
3. Feature blueprints live under `app/main`, `app/auth`, and `app/admin`.
4. API resources live under `app/api/resources` and are registered from `app/api/__init__.py`.

## Package Responsibilities

- `app/main`: public pages, project display, contact form.
- `app/auth`: Flask-Login based admin login/logout.
- `app/admin`: authenticated admin dashboard and CRUD screens.
- `app/api`: JSON API resources and JWT helper functions.
- `app/models`: SQLAlchemy models and serialization helpers.
- `app/forms`: WTForms validation for browser forms.
- `app/services`: side-effect integrations such as email.
- `app/errors`: application error handlers.
- `app/utils`: reusable helpers for validation and file handling.

## Design Notes

The project intentionally stays monolithic because the product scope is a personal portfolio CMS. The current structure keeps code interview-friendly without introducing unnecessary service boundaries.
