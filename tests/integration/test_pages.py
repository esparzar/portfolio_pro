def test_public_pages_load(client):
    for path in ["/", "/about", "/projects", "/contact", "/health"]:
        response = client.get(path)
        assert response.status_code == 200


def test_missing_page_uses_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404


def test_contact_form_submission(client, app):
    response = client.post(
        "/contact",
        data={
            "name": "John Doe",
            "email": "john@example.com",
            "service": "other",
            "message": "This is a test message for the contact form.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
