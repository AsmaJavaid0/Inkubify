from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.services.completion import compute_profile_completion
from tests.conftest import make_test_token


def test_patch_rejects_unknown_fields(client: TestClient) -> None:
    token = make_test_token()
    res = client.patch(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "hacked"},
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "validation_error"


def test_patch_rejects_under_18(client: TestClient) -> None:
    token = make_test_token()
    under_18_dob = (date.today() - timedelta(days=365 * 16)).isoformat()
    res = client.patch(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"date_of_birth": under_18_dob},
    )
    assert res.status_code == 422
    assert "date_of_birth" in res.json()["error"]["fields"]


def test_patch_rejects_province_city_mismatch(client: TestClient) -> None:
    token = make_test_token()
    res = client.patch(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"province": "Sindh", "city": "Lahore"},
    )
    assert res.status_code == 422


def test_patch_rejects_business_model_for_category(client: TestClient) -> None:
    token = make_test_token()
    res = client.patch(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"business_category": "ecommerce", "business_model": "b2c"},
    )
    assert res.status_code == 422


def test_full_wizard_and_completion(client: TestClient) -> None:
    token = make_test_token()
    headers = {"Authorization": f"Bearer {token}"}

    res_fail = client.post("/api/v1/profiles/me/onboarding/complete", headers=headers)
    assert res_fail.status_code == 422
    assert "date_of_birth" in res_fail.json()["error"]["fields"]
    assert "skills" in res_fail.json()["error"]["fields"]

    r1 = client.patch(
        "/api/v1/profiles/me",
        headers=headers,
        json={
            "full_name": "Asma Khan",
            "date_of_birth": "1998-05-15",
            "province": "Punjab",
            "city": "Lahore",
            "preferred_language": "en",
            "bio": "Building an e-commerce store",
            "onboarding_step": 2,
        },
    )
    assert r1.status_code == 200
    assert r1.json()["onboarding"]["status"] == "in_progress"
    assert r1.json()["onboarding"]["step"] == 2

    r2 = client.patch(
        "/api/v1/profiles/me",
        headers=headers,
        json={
            "education_level": "bachelors",
            "occupation_status": "freelancer",
            "prior_business": "none",
            "onboarding_step": 3,
        },
    )
    assert r2.status_code == 200

    r3 = client.put(
        "/api/v1/profiles/me/skills",
        headers=headers,
        json={"skills": [{"skill_id": 1, "proficiency": "intermediate"}]},
    )
    assert r3.status_code == 200
    assert len(r3.json()["skills"]) == 1

    r3_details = client.patch(
        "/api/v1/profiles/me",
        headers=headers,
        json={
            "experience_level": "intermediate",
            "experience_years": 2,
            "availability": "part_time",
            "linkedin_url": "https://www.linkedin.com/in/asmajavaid",
            "github_url": "https://github.com/asmajavaid",
            "onboarding_step": 4,
        },
    )
    assert r3_details.status_code == 200

    r4 = client.patch(
        "/api/v1/profiles/me",
        headers=headers,
        json={
            "business_category": "ecommerce",
            "business_model": "d2c",
            "target_audience": ["individual_consumers"],
            "primary_goal": "Launch an online clothing store and validate demand.",
            "expected_business_timeline": "3_6_months",
            "available_budget_pkr": 150000,
            "available_resources": ["laptop_computer", "internet"],
            "team_members": 1,
            "resource_info": ["personal_savings"],
            "onboarding_step": 5,
        },
    )
    assert r4.status_code == 200

    r_done = client.post("/api/v1/profiles/me/onboarding/complete", headers=headers)
    assert r_done.status_code == 200
    data = r_done.json()
    assert data["onboarding"]["status"] == "completed"
    assert data["onboarding"]["completed_at"] is not None
    assert data["profile_completion"] == 100


def test_completion_formula_bounds() -> None:
    empty = {"preferred_language": "en"}
    assert compute_profile_completion(empty, 0) == 6
    full_required = {
        "date_of_birth": "1998-01-01",
        "province": "Punjab",
        "city": "Lahore",
        "preferred_language": "en",
        "education_level": "bachelors",
        "occupation_status": "student",
        "prior_business": "none",
        "experience_level": "intermediate",
        "availability": "part_time",
        "business_category": "ecommerce",
        "business_model": "b2b",
        "primary_goal": "Build a sustainable online store",
        "expected_business_timeline": "3_6_months",
    }
    assert compute_profile_completion(full_required, 1) == 100
