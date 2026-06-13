import pytest

from app import create_app, db
from app.models.user import User


@pytest.fixture()
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def admin_user(app):
    with app.app_context():
        user = User(username="admin", email="admin@example.com", is_admin=True, is_active=True)
        user.set_password("admin-password")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def user(app):
    with app.app_context():
        user = User(username="member", email="member@example.com", is_admin=False, is_active=True)
        user.set_password("member-password")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def auth_headers(client, admin_user):
    response = client.post(
        "/api/auth",
        json={"username": "admin", "password": "admin-password"},
    )
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
