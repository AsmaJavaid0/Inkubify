from datetime import date
from typing import Any

from app.utils.validators import validate_date_of_birth, validate_province_and_city


def compute_profile_completion(profile: dict[str, Any], skills_count: int) -> int:
    """Compute founder-profile completion from the four profile sections."""
    score = 0.0

    # Personal information (25%)
    for field in ("date_of_birth", "province", "city", "preferred_language"):
        if profile.get(field):
            score += 6.25

    # Education and background (15%)
    for field in ("education_level", "occupation_status", "prior_business"):
        if profile.get(field):
            score += 5.0

    # Skills and expertise (20%)
    if skills_count >= 1 or profile.get("other_skills"):
        score += 10.0
    if profile.get("experience_level"):
        score += 5.0
    if profile.get("availability"):
        score += 5.0

    # Business interests (40%)
    for field in (
        "business_category",
        "business_model",
        "primary_goal",
        "expected_business_timeline",
    ):
        if profile.get(field):
            score += 10.0

    return int(max(0, min(100, round(score))))


def validate_onboarding_complete(profile: dict[str, Any], skills_count: int) -> dict[str, str]:
    """Return a map of missing or invalid required founder-profile fields."""
    errors: dict[str, str] = {}

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
    if not profile.get("education_level"):
        errors["education_level"] = "Education level is required"
    if not profile.get("occupation_status"):
        errors["occupation_status"] = "Current occupation is required"
    if not profile.get("prior_business"):
        errors["prior_business"] = "Please select your previous business experience"

    if skills_count < 1 and not profile.get("other_skills"):
        errors["skills"] = "Select at least one technical skill or describe your other skills"
    if not profile.get("experience_level"):
        errors["experience_level"] = "Please select your experience level"
    if not profile.get("availability"):
        errors["availability"] = "Please select your availability"

    if not profile.get("business_category"):
        errors["business_category"] = "Please select a business category"
    if not profile.get("business_model"):
        errors["business_model"] = "Please select a business model"
    if not profile.get("primary_goal"):
        errors["primary_goal"] = "Please describe your primary business goal"
    if not profile.get("expected_business_timeline"):
        errors["expected_business_timeline"] = "Please select your expected business timeline"

    category = profile.get("business_category")
    model = profile.get("business_model")
    if category == "ecommerce" and model not in ("b2b", "d2c", "dropshipping"):
        errors["business_model"] = "Choose a valid e-commerce business model"
    elif category == "technology_based" and model not in ("b2b", "b2c"):
        errors["business_model"] = "Choose a valid technology business model"

    return errors
