from datetime import date
from typing import Any

from app.utils.validators import validate_date_of_birth, validate_province_and_city


def compute_profile_completion(profile: dict[str, Any], skills_count: int) -> int:
    """
    Compute founder profile completion percentage (0..100).

    Required step weights (total 100 base):
      - Personal (25): date_of_birth, province, city, preferred_language (6.25 each)
      - Background (25): education_level, occupation_status, work_experience,
        prior_business (6.25 each)
      - Skills (25): >= 1 skill selected (25)
      - Goals (25): primary_goal, weekly_hours (12.5 each)

    Optional bonus (up to +10, capped at 100 total):
      - avatar_url (+2.5)
      - bio (+2.5)
      - field_of_study (+2.5)
      - instagram_url or linkedin_url (+2.5)
    """
    score = 0.0

    # Personal (25)
    for field in ("date_of_birth", "province", "city", "preferred_language"):
        if profile.get(field):
            score += 6.25

    # Background (25)
    for field in ("education_level", "occupation_status", "work_experience", "prior_business"):
        if profile.get(field):
            score += 6.25

    # Skills (25)
    if skills_count >= 1:
        score += 25.0

    # Goals (25)
    for field in ("primary_goal", "weekly_hours"):
        if profile.get(field):
            score += 12.5

    # Optional bonus (capped at +10, total <= 100)
    bonus = 0.0
    if profile.get("avatar_url"):
        bonus += 2.5
    if profile.get("bio"):
        bonus += 2.5
    if profile.get("field_of_study"):
        bonus += 2.5
    if profile.get("instagram_url") or profile.get("linkedin_url"):
        bonus += 2.5

    total = round(min(100.0, score + min(10.0, bonus)))
    return int(max(0, min(100, total)))


def validate_onboarding_complete(profile: dict[str, Any], skills_count: int) -> dict[str, str]:
    """Return a map of missing/invalid required fields for completing onboarding."""
    errors: dict[str, str] = {}

    # Step 1: Personal
    dob_raw = profile.get("date_of_birth")
    if not dob_raw:
        errors["date_of_birth"] = "Date of birth is required"
    else:
        try:
            dob = dob_raw if isinstance(dob_raw, date) else date.fromisoformat(str(dob_raw))
            validate_date_of_birth(dob)
        except ValueError as exc:
            errors["date_of_birth"] = str(exc)

    province = profile.get("province")
    city = profile.get("city")
    if not province:
        errors["province"] = "Province or territory is required"
    if not city:
        errors["city"] = "City is required"
    if province and city:
        try:
            validate_province_and_city(province, city)
        except ValueError as exc:
            errors["city"] = str(exc)

    if not profile.get("preferred_language"):
        errors["preferred_language"] = "Preferred language is required"

    # Step 2: Background
    if not profile.get("education_level"):
        errors["education_level"] = "Education level is required"
    if not profile.get("occupation_status"):
        errors["occupation_status"] = "Current status is required"
    if not profile.get("work_experience"):
        errors["work_experience"] = "Work experience is required"
    if not profile.get("prior_business"):
        errors["prior_business"] = "Prior business experience is required"

    # Step 3: Skills
    if skills_count < 1:
        errors["skills"] = "Please select at least 1 skill"
    elif skills_count > 10:
        errors["skills"] = "You can select up to 10 skills"

    # Step 4: Goals
    if not profile.get("primary_goal"):
        errors["primary_goal"] = "Primary goal is required"
    if not profile.get("weekly_hours"):
        errors["weekly_hours"] = "Weekly time available is required"

    return errors
