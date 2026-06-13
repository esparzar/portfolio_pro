from app import db
from app.models.contact import Contact
from app.models.project import Project


def test_api_contact_submission(client, app):
    response = client.post(
        "/api/contacts",
        json={
            "name": "API User",
            "email": "api@example.com",
            "service": "other",
            "message": "Testing API contact submission",
        },
    )

    assert response.status_code == 201
    with app.app_context():
        assert Contact.query.filter_by(email="api@example.com").first() is not None


def test_api_contact_rejects_invalid_email(client):
    response = client.post(
        "/api/contacts",
        json={"name": "API User", "email": "invalid", "message": "Testing invalid email"},
    )

    assert response.status_code == 400


def test_api_projects_list_and_detail(client, app):
    with app.app_context():
        project = Project(title="API Project", description="Project API test", featured=True)
        db.session.add(project)
        db.session.commit()
        project_id = project.id

    list_response = client.get("/api/projects")
    detail_response = client.get(f"/api/projects/{project_id}")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert detail_response.get_json()["project"]["title"] == "API Project"


def test_api_auth_and_admin_contact_list(client, auth_headers):
    response = client.get("/api/contacts", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json()["success"] is True


def test_api_rejects_missing_project(client):
    response = client.get("/api/projects/99999")
    assert response.status_code == 404
