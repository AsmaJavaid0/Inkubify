from fastapi.testclient import TestClient


def test_username_login_rejects_reserved_username(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Password1"},
    )
    assert response.status_code == 422


def test_username_login_does_not_reveal_unknown_accounts(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "unknown_founder", "password": "Password1"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid username or password"
