from fastapi.testclient import TestClient

from tests.conftest import make_test_token


def test_missing_bearer_token_returns_401(client: TestClient) -> None:
    res = client.get("/api/v1/profiles/me")
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "unauthorized"


def test_expired_token_returns_401(client: TestClient) -> None:
    token = make_test_token(exp_offset=-60)
    res = client.get("/api/v1/profiles/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "unauthorized"


def test_wrong_audience_returns_401(client: TestClient) -> None:
    token = make_test_token(aud="anon")
    res = client.get("/api/v1/profiles/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401


def test_valid_token_succeeds(client: TestClient) -> None:
    token = make_test_token()
    res = client.get("/api/v1/profiles/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "asma_k"
