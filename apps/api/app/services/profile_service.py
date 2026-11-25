from datetime import UTC, datetime
from typing import Any

from supabase import Client

from app.core.security import AuthenticatedUser
from app.schemas.catalog import ProfileSkillOut, SkillCatalogItem
from app.schemas.common import ApiError
from app.schemas.profile import (
    OnboardingInfo,
    ProfilePatchRequest,
    ProfileResponse,
    ProfileSkillsPutRequest,
)
from app.services.completion import compute_profile_completion, validate_onboarding_complete
from app.utils.validators import validate_province_and_city


def _build_profile_response(
    row: dict[str, Any],
    skills_rows: list[dict[str, Any]],
    email: str | None,
) -> ProfileResponse:
    skills: list[ProfileSkillOut] = []
    for item in skills_rows:
        skill_meta = item.get("skills") or {}
        if not isinstance(skill_meta, dict):
            continue
        skills.append(
            ProfileSkillOut(
                skill_id=item["skill_id"],
                slug=skill_meta.get("slug", ""),
                name=skill_meta.get("name", ""),
                proficiency=item["proficiency"],
            )
        )

    return ProfileResponse(
        id=str(row["id"]),
        username=str(row["username"]),
        full_name=row["full_name"],
        email=email,
        phone_e164=row["phone_e164"],
        country_code=row["country_code"],
        avatar_url=row.get("avatar_url"),
        date_of_birth=row.get("date_of_birth"),
        gender=row.get("gender"),
        province=row.get("province"),
        city=row.get("city"),
        bio=row.get("bio"),
        preferred_language=row.get("preferred_language", "en"),
        education_level=row.get("education_level"),
        field_of_study=row.get("field_of_study"),
        occupation_status=row.get("occupation_status"),
        work_experience=row.get("work_experience"),
        prior_business=row.get("prior_business"),
        primary_goal=row.get("primary_goal"),
        weekly_hours=row.get("weekly_hours"),
        interested_in=row.get("interested_in") or [],
        instagram_url=row.get("instagram_url"),
        linkedin_url=row.get("linkedin_url"),
        skills=skills,
        onboarding=OnboardingInfo(
            status=row.get("onboarding_status", "not_started"),
            step=int(row.get("onboarding_step", 1)),
            completed_at=row.get("onboarding_completed_at"),
        ),
        profile_completion=int(row.get("profile_completion", 0)),
    )


def _fetch_profile_and_skills(
    user_db: Client, user_id: str
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    prof_res = (
        user_db.table("profiles")
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    if not prof_res.data:
        raise ApiError(status_code=404, code="not_found", message="Profile not found")

    skills_res = (
        user_db.table("profile_skills")
        .select("skill_id, proficiency, skills(id, slug, name, category)")
        .eq("profile_id", user_id)
        .execute()
    )
    return prof_res.data[0], (skills_res.data or [])


def list_active_skills(user_db: Client) -> list[SkillCatalogItem]:
    res = (
        user_db.table("skills")
        .select("id, slug, name, category")
        .eq("is_active", True)
        .order("sort_order")
        .execute()
    )
    return [SkillCatalogItem(**row) for row in (res.data or [])]


def get_my_profile(user_db: Client, user: AuthenticatedUser) -> ProfileResponse:
    row, skills_rows = _fetch_profile_and_skills(user_db, user.id)
    return _build_profile_response(row, skills_rows, user.email)


def patch_my_profile(
    user_db: Client,
    service_db: Client,
    user: AuthenticatedUser,
    payload: ProfilePatchRequest,
) -> ProfileResponse:
    existing, skills_rows = _fetch_profile_and_skills(user_db, user.id)
    raw_updates = payload.model_dump(mode="json", exclude_unset=True)

    # Validate merged province + city consistency
    effective_province = (
        raw_updates["province"] if "province" in raw_updates else existing.get("province")
    )
    effective_city = raw_updates["city"] if "city" in raw_updates else existing.get("city")
    try:
        validate_province_and_city(effective_province, effective_city)
    except ValueError as exc:
        raise ApiError(
            status_code=422,
            code="validation_error",
            message="Validation failed",
            fields={"city": str(exc)},
        ) from exc

    # Separate editable columns (user-JWT RLS update) from server-protected columns
    user_updates: dict[str, Any] = {}
    for key, val in raw_updates.items():
        if key == "onboarding_step":
            current_step = int(existing.get("onboarding_step", 1))
            if val is not None and val >= current_step:
                user_updates["onboarding_step"] = val
        else:
            user_updates[key] = val

    if user_updates:
        user_db.table("profiles").update(user_updates).eq("id", user.id).execute()

    merged = {**existing, **user_updates}
    new_completion = compute_profile_completion(merged, len(skills_rows))
    system_updates: dict[str, Any] = {"profile_completion": new_completion}
    if existing.get("onboarding_status") == "not_started":
        system_updates["onboarding_status"] = "in_progress"

    service_db.table("profiles").update(system_updates).eq("id", user.id).execute()

    updated_row, updated_skills = _fetch_profile_and_skills(user_db, user.id)
    return _build_profile_response(updated_row, updated_skills, user.email)


def replace_my_skills(
    user_db: Client,
    service_db: Client,
    user: AuthenticatedUser,
    payload: ProfileSkillsPutRequest,
) -> ProfileResponse:
    existing, _ = _fetch_profile_and_skills(user_db, user.id)

    skill_ids = [item.skill_id for item in payload.skills]
    catalog_res = (
        user_db.table("skills")
        .select("id")
        .eq("is_active", True)
        .in_("id", skill_ids)
        .execute()
    )
    valid_ids = {row["id"] for row in (catalog_res.data or [])}
    invalid_ids = [sid for sid in skill_ids if sid not in valid_ids]
    if invalid_ids:
        raise ApiError(
            status_code=422,
            code="validation_error",
            message="One or more selected skills are invalid",
            fields={"skills": "Invalid skill selection"},
        )

    # Replace via user-JWT client (RLS enforced)
    user_db.table("profile_skills").delete().eq("profile_id", user.id).execute()
    rows_to_insert = [
        {
            "profile_id": user.id,
            "skill_id": item.skill_id,
            "proficiency": item.proficiency.value,
        }
        for item in payload.skills
    ]
    user_db.table("profile_skills").insert(rows_to_insert).execute()

    new_completion = compute_profile_completion(existing, len(rows_to_insert))
    system_updates: dict[str, Any] = {"profile_completion": new_completion}
    if existing.get("onboarding_status") == "not_started":
        system_updates["onboarding_status"] = "in_progress"
    service_db.table("profiles").update(system_updates).eq("id", user.id).execute()

    updated_row, updated_skills = _fetch_profile_and_skills(user_db, user.id)
    return _build_profile_response(updated_row, updated_skills, user.email)


def complete_my_onboarding(
    user_db: Client,
    service_db: Client,
    user: AuthenticatedUser,
) -> ProfileResponse:
    existing, skills_rows = _fetch_profile_and_skills(user_db, user.id)
    field_errors = validate_onboarding_complete(existing, len(skills_rows))
    if field_errors:
        raise ApiError(
            status_code=422,
            code="validation_error",
            message="Please complete all required profile fields before finishing",
            fields=field_errors,
        )

    completion = compute_profile_completion(existing, len(skills_rows))
    completed_at = existing.get("onboarding_completed_at") or datetime.now(UTC).isoformat()

    user_db.table("profiles").update({"onboarding_step": 5}).eq("id", user.id).execute()
    service_db.table("profiles").update(
        {
            "onboarding_status": "completed",
            "onboarding_completed_at": completed_at,
            "profile_completion": completion,
        }
    ).eq("id", user.id).execute()

    updated_row, updated_skills = _fetch_profile_and_skills(user_db, user.id)
    return _build_profile_response(updated_row, updated_skills, user.email)
