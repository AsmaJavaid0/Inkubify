from fastapi.testclient import TestClient


def test_username_available(client: TestClient) -> None:
    res = client.get("/api/v1/usernames/availability?username=new_founder")
    assert res.status_code == 200
    assert res.json() == {"available": True}


def test_username_taken(client: TestClient) -> None:
    res = client.get("/api/v1/usernames/availability?username=ASMA_K")
    assert res.status_code == 200
    assert res.json() == {"available": False}


def test_username_reserved_rejected(client: TestClient) -> None:
    res = client.get("/api/v1/usernames/availability?username=admin")
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "validation_error"


def test_username_invalid_format_rejected(client: TestClient) -> None:
    res = client.get("/api/v1/usernames/availability?username=1abc")
    assert res.status_code == 422
    assert "username" in res.json()["error"]["fields"]


def test_username_rate_limited(client: TestClient) -> None:
    from app.api.v1.endpoints.usernames import limiter

    limiter.reset()
    try:
        for _ in range(20):
            r = client.get("/api/v1/usernames/availability?username=valid_name_check")
            assert r.status_code == 200
        blocked = client.get("/api/v1/usernames/availability?username=valid_name_check")
        assert blocked.status_code == 429
        assert blocked.json()["error"]["code"] == "rate_limited"
    finally:
        limiter.reset()
