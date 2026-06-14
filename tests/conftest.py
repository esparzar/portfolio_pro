from collections.abc import Iterator
from typing import cast

import pytest
from click.testing import CliRunner
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from app.models.user import User


@pytest.fixture()
def app() -> Iterator[Flask]:
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> CliRunner:
    return app.test_cli_runner()


@pytest.fixture()
def admin_user(app: Flask) -> int:
    with app.app_context():
        user = User(username="admin", email="admin@example.com", is_admin=True, is_active=True)
        user.set_password("admin-password")
        db.session.add(user)
        db.session.commit()
        return cast(int, user.id)


@pytest.fixture()
def user(app: Flask) -> int:
    with app.app_context():
        user = User(username="member", email="member@example.com", is_admin=False, is_active=True)
        user.set_password("member-password")
        db.session.add(user)
        db.session.commit()
        return cast(int, user.id)


@pytest.fixture()
def auth_headers(client: FlaskClient, admin_user: int) -> dict[str, str]:
    response = client.post(
        "/api/auth",
        json={"username": "admin", "password": "admin-password"},
    )
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
