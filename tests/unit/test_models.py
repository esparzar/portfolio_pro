from flask import Flask

from app import db
from app.models.contact import Contact
from app.models.project import Project
from app.models.user import User


def test_user_password_hashing(app: Flask) -> None:
    user = User(username="hashuser", email="hash@example.com")
    user.set_password("mypassword")

    assert user.password_hash != "mypassword"
    assert user.check_password("mypassword") is True
    assert user.check_password("wrong") is False


def test_user_authentication_updates_last_login(app: Flask) -> None:
    with app.app_context():
        user = User(username="authuser", email="auth@example.com", is_active=True)
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

        authenticated = User.authenticate("authuser", "secret123")

        assert authenticated is not None
        assert authenticated.username == "authuser"
        assert authenticated.last_login is not None
        assert User.authenticate("authuser", "wrong") is None


def test_project_serialization_and_technology_parsing(app: Flask) -> None:
    with app.app_context():
        project = Project(
            title="Test Project",
            description="Test description",
            technologies="Python, Flask, SQLAlchemy",
            featured=True,
            status="completed",
        )
        db.session.add(project)
        db.session.commit()

        data = project.to_dict()

        assert data["title"] == "Test Project"
        assert data["featured"] is True
        assert project.get_technologies_list() == ["Python", "Flask", "SQLAlchemy"]


def test_project_query_helpers(app: Flask) -> None:
    with app.app_context():
        db.session.add_all(
            [
                Project(title="Featured", description="Test", featured=True, display_order=1),
                Project(title="Regular", description="Test", featured=False, display_order=2),
            ]
        )
        db.session.commit()

        assert len(Project.get_featured()) == 1
        assert len(Project.get_all_active()) == 2


def test_contact_helpers(app: Flask) -> None:
    with app.app_context():
        contact = Contact(
            name="Reader", email="reader@example.com", message="Please read this message"
        )
        db.session.add(contact)
        db.session.commit()

        assert Contact.get_unread()[0].email == "reader@example.com"
        assert Contact.mark_as_read(contact.id) is True
        db.session.refresh(contact)
        assert contact.is_read is True
        assert contact.to_dict()["email"] == "reader@example.com"
