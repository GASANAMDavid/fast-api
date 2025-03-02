def test_login(create_test_user, client):
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_article(client, access_token):
    response = client.post(
        "/articles/",
        json={"title": "Test Article", "description": "Test Description"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Article"


def test_read_articles(client, access_token):
    response = client.get(
        "/articles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_article(client, access_token):
    response = client.put(
        "/articles/1",
        json={"title": "Updated Article", "description": "Updated Description"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Article"


def test_delete_article(client, access_token):
    response = client.delete(
        "/articles/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
