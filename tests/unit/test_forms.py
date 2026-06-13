from app.forms.auth import LoginForm, RegisterForm
from app.forms.contact import ContactForm
from app.forms.projects import ProjectForm


def test_login_form_validation(app):
    with app.test_request_context(
        method="POST", data={"username": "admin", "password": "secret123"}
    ):
        assert LoginForm().validate() is True


def test_contact_form_requires_valid_email(app):
    with app.test_request_context(
        method="POST",
        data={
            "name": "Jane",
            "email": "not-email",
            "service": "other",
            "message": "A valid length message",
        },
    ):
        assert ContactForm().validate() is False


def test_project_form_accepts_valid_urls(app):
    with app.test_request_context(
        method="POST",
        data={
            "title": "Portfolio Pro",
            "description": "Professional Flask portfolio",
            "short_description": "Portfolio",
            "github_url": "https://github.com/example/portfolio",
            "project_url": "https://example.com",
            "status": "completed",
            "display_order": 1,
        },
    ):
        assert ProjectForm().validate() is True


def test_register_form_validation(app):
    with app.test_request_context(
        method="POST",
        data={"username": "newuser", "email": "new@example.com", "password": "password123"},
    ):
        assert RegisterForm().validate() is True
