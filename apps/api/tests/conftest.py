import time
from collections.abc import Generator
from typing import Any

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app

TEST_JWT_SECRET = "test-super-secret-hs256-key-at-least-32-bytes"
TEST_SUPABASE_URL = "https://example.supabase.co"


def make_test_token(
    user_id: str = "11111111-1111-1111-1111-111111111111",
    email: str = "founder@example.com",
    exp_offset: int = 3600,
    aud: str = "authenticated",
    iss: str = f"{TEST_SUPABASE_URL}/auth/v1",
) -> str:
    now = int(time.time())
    payload = {
        "sub": user_id,
        "email": email,
        "aud": aud,
        "iss": iss,
        "role": "authenticated",
        "iat": now,
        "exp": now + exp_offset,
    }
    return jwt.encode(payload, TEST_JWT_SECRET, algorithm="HS256")


class FakeQueryResult:
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.data = data


class FakeTableQuery:
    def __init__(self, store: dict[str, list[dict[str, Any]]], table: str) -> None:
        self.store = store
        self.table = table
        self._op = "select"
        self._filters: list[tuple[str, str, Any]] = []
        self._payload: Any = None
        self._limit: int | None = None

    def select(self, *_args: Any, **_kwargs: Any) -> "FakeTableQuery":
        self._op = "select"
        return self

    def insert(self, payload: Any) -> "FakeTableQuery":
        self._op = "insert"
        self._payload = payload
        return self

    def update(self, payload: dict[str, Any]) -> "FakeTableQuery":
        self._op = "update"
        self._payload = payload
        return self

    def delete(self) -> "FakeTableQuery":
        self._op = "delete"
        return self

    def eq(self, col: str, val: Any) -> "FakeTableQuery":
        self._filters.append(("eq", col, val))
        return self

    def in_(self, col: str, vals: list[Any]) -> "FakeTableQuery":
        self._filters.append(("in", col, set(vals)))
        return self

    def order(self, *_args: Any, **_kwargs: Any) -> "FakeTableQuery":
        return self

    def limit(self, n: int) -> "FakeTableQuery":
        self._limit = n
        return self

    def _matches(self, row: dict[str, Any]) -> bool:
        for op, col, val in self._filters:
            if op == "eq" and str(row.get(col)) != str(val):
                return False
            if op == "in" and row.get(col) not in val:
                return False
        return True

    def execute(self) -> FakeQueryResult:
        rows = self.store.setdefault(self.table, [])
        if self._op == "select":
            matched = [dict(r) for r in rows if self._matches(r)]
            if self.table == "profile_skills":
                skills_by_id = {s["id"]: s for s in self.store.get("skills", [])}
                for item in matched:
                    item["skills"] = skills_by_id.get(item["skill_id"], {})
            if self._limit is not None:
                matched = matched[: self._limit]
            return FakeQueryResult(matched)
        if self._op == "insert":
            items = self._payload if isinstance(self._payload, list) else [self._payload]
            rows.extend(dict(i) for i in items)
            return FakeQueryResult(items)
        if self._op == "update":
            updated = []
            for row in rows:
                if self._matches(row):
                    row.update(self._payload)
                    updated.append(dict(row))
            return FakeQueryResult(updated)
        if self._op == "delete":
            remaining = [r for r in rows if not self._matches(r)]
            self.store[self.table] = remaining
            return FakeQueryResult([])
        return FakeQueryResult([])


class FakeSupabaseClient:
    def __init__(self, store: dict[str, list[dict[str, Any]]]) -> None:
        self.store = store

    def table(self, name: str) -> FakeTableQuery:
        return FakeTableQuery(self.store, name)


@pytest.fixture()
def test_settings() -> Settings:
    return Settings(
        APP_ENV="test",
        WEB_ORIGIN="http://localhost:3000",
        SUPABASE_URL=TEST_SUPABASE_URL,
        SUPABASE_ANON_KEY="test-anon-key",
        SUPABASE_SERVICE_ROLE_KEY="test-service-role-key",
        SUPABASE_JWT_SECRET=TEST_JWT_SECRET,
        RATE_LIMIT_USERNAME_CHECK="20/minute",
    )


@pytest.fixture()
def fake_store() -> dict[str, list[dict[str, Any]]]:
    return {
        "profiles": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "username": "asma_k",
                "full_name": "Asma Khan",
                "phone_e164": "+923001234567",
                "country_code": "PK",
                "avatar_url": None,
                "date_of_birth": None,
                "gender": None,
                "address": None,
                "province": None,
                "city": None,
                "bio": None,
                "preferred_language": "en",
                "education_level": None,
                "field_of_study": None,
                "occupation_status": None,
                "prior_business": None,
                "other_skills": None,
                "experience_level": None,
                "experience_years": None,
                "portfolio_url": None,
                "linkedin_url": None,
                "github_url": None,
                "availability": None,
                "business_category": None,
                "business_model": None,
                "target_audience": [],
                "primary_goal": None,
                "expected_business_timeline": None,
                "available_budget_pkr": None,
                "available_resources": [],
                "team_members": None,
                "resource_info": [],
                "onboarding_status": "not_started",
                "onboarding_step": 1,
                "profile_completion": 0,
                "onboarding_completed_at": None,
            }
        ],
        "skills": [
            {
                "id": 1,
                "slug": "digital-marketing",
                "name": "Digital Marketing",
                "category": "Marketing & Sales",
                "sort_order": 10,
                "is_active": True,
            },
            {
                "id": 2,
                "slug": "web-dev",
                "name": "Web Development",
                "category": "Technology",
                "sort_order": 20,
                "is_active": True,
            },
            {
                "id": 3,
                "slug": "finance",
                "name": "Accounting & Finance",
                "category": "Operations & Finance",
                "sort_order": 30,
                "is_active": True,
            },
        ],
        "profile_skills": [],
    }


@pytest.fixture()
def client(
    test_settings: Settings, fake_store: dict[str, list[dict[str, Any]]]
) -> Generator[TestClient, None, None]:
    from app.api.deps import get_service_db, get_user_db
    from app.core.config import get_settings

    app = create_app(test_settings)
    fake_db = FakeSupabaseClient(fake_store)
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_user_db] = lambda: fake_db
    app.dependency_overrides[get_service_db] = lambda: fake_db

    with TestClient(app) as tc:
        yield tc
