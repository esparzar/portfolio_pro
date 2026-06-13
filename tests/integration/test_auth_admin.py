def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_admin_dashboard_requires_login(client):
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_login_success(client, admin_user):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin-password"},
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_non_admin_cannot_access_admin(client, user):
    client.post("/auth/login", data={"username": "member", "password": "member-password"})

    response = client.get("/admin/", follow_redirects=True)

    assert response.status_code == 200
