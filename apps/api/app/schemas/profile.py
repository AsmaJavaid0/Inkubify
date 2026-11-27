from datetime import date, datetime
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.catalog import ProfileSkillOut
from app.schemas.common import (
    AvailabilityEnum,
    AvailableResourceEnum,
    BusinessCategoryEnum,
    BusinessModelEnum,
    BusinessTimelineEnum,
    EducationEnum,
    GenderEnum,
    LanguageEnum,
    OccupationEnum,
    OnboardingStatusEnum,
    PriorBusinessEnum,
    ProficiencyEnum,
    ResourceInfoEnum,
    TargetAudienceEnum,
)
from app.utils.validators import (
    normalize_full_name,
    validate_date_of_birth,
    validate_linkedin_url,
    validate_province_and_city,
)


def _normalize_http_url(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    candidate = cleaned if cleaned.startswith(("http://", "https://")) else f"https://{cleaned}"
    parsed = urlparse(candidate)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError(f"{field_name} must be a valid http(s) URL")
    return candidate


class ProfilePatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = None
    avatar_url: str | None = None
    date_of_birth: date | None = None
    gender: GenderEnum | None = None
    address: str | None = None
    province: str | None = None
    city: str | None = None
    bio: str | None = None
    preferred_language: LanguageEnum | None = None

    education_level: EducationEnum | None = None
    field_of_study: str | None = None
    occupation_status: OccupationEnum | None = None
    prior_business: PriorBusinessEnum | None = None

    other_skills: str | None = None
    experience_level: ProficiencyEnum | None = None
    experience_years: int | None = Field(default=None, ge=0, le=60)
    portfolio_url: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    availability: AvailabilityEnum | None = None

    business_category: BusinessCategoryEnum | None = None
    business_model: BusinessModelEnum | None = None
    target_audience: list[TargetAudienceEnum] | None = None
    primary_goal: str | None = None
    expected_business_timeline: BusinessTimelineEnum | None = None

    available_budget_pkr: int | None = Field(default=None, ge=0, le=1_000_000_000_000)
    available_resources: list[AvailableResourceEnum] | None = None
    team_members: int | None = Field(default=None, ge=0, le=100)
    resource_info: list[ResourceInfoEnum] | None = None

    onboarding_step: int | None = Field(default=None, ge=1, le=5)

    @field_validator("full_name")
    @classmethod
    def check_full_name(cls, value: str | None) -> str | None:
        return normalize_full_name(value) if value is not None else None

    @field_validator("avatar_url")
    @classmethod
    def check_avatar_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        if not cleaned.startswith(("https://", "http://")) or len(cleaned) > 500:
            raise ValueError("Avatar URL must be a valid http(s) URL under 500 characters")
        return cleaned

    @field_validator("date_of_birth")
    @classmethod
    def check_dob(cls, value: date | None) -> date | None:
        return validate_date_of_birth(value) if value is not None else None

    @field_validator("address")
    @classmethod
    def check_address(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        if len(cleaned) > 250:
            raise ValueError("Address must be 250 characters or fewer")
        return cleaned

    @field_validator("bio")
    @classmethod
    def check_bio(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        if len(cleaned) > 280:
            raise ValueError("Bio must be 280 characters or fewer")
        return cleaned

    @field_validator("field_of_study")
    @classmethod
    def check_field_of_study(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        if not (2 <= len(cleaned) <= 80):
            raise ValueError("Field of study must be between 2 and 80 characters")
        return cleaned

    @field_validator("other_skills")
    @classmethod
    def check_other_skills(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        if len(cleaned) > 1000:
            raise ValueError("Other skills must be 1000 characters or fewer")
        return cleaned

    @field_validator("primary_goal")
    @classmethod
    def check_primary_goal(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        if len(cleaned) > 500:
            raise ValueError("Primary goal must be 500 characters or fewer")
        return cleaned

    @field_validator("portfolio_url")
    @classmethod
    def check_portfolio_url(cls, value: str | None) -> str | None:
        return _normalize_http_url(value, "Portfolio URL")

    @field_validator("linkedin_url")
    @classmethod
    def check_linkedin(cls, value: str | None) -> str | None:
        return validate_linkedin_url(value)

    @field_validator("github_url")
    @classmethod
    def check_github_url(cls, value: str | None) -> str | None:
        cleaned = _normalize_http_url(value, "GitHub URL")
        if cleaned and (urlparse(cleaned).hostname or "").lower() not in ("github.com", "www.github.com"):
            raise ValueError("GitHub URL must point to github.com")
        return cleaned

    @field_validator("target_audience", "available_resources", "resource_info")
    @classmethod
    def deduplicate_selections(cls, value):
        return list(dict.fromkeys(value)) if value is not None else None

    @model_validator(mode="after")
    def check_location_and_business_model(self) -> "ProfilePatchRequest":
        province, city = validate_province_and_city(self.province, self.city)
        if "province" in self.model_fields_set:
            self.province = province
        if "city" in self.model_fields_set:
            self.city = city
        if self.business_category and self.business_model:
            allowed = {
                BusinessCategoryEnum.ecommerce: {
                    BusinessModelEnum.b2b,
                    BusinessModelEnum.d2c,
                    BusinessModelEnum.dropshipping,
                },
                BusinessCategoryEnum.technology_based: {
                    BusinessModelEnum.b2b,
                    BusinessModelEnum.b2c,
                },
            }
            if self.business_model not in allowed[self.business_category]:
                raise ValueError("The selected business model does not match the business category")
        return self


class SkillItemInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: int = Field(gt=0)
    proficiency: ProficiencyEnum


class ProfileSkillsPutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skills: list[SkillItemInput] = Field(min_length=1, max_length=10)

    @model_validator(mode="after")
    def check_unique_skills(self) -> "ProfileSkillsPutRequest":
        ids = [item.skill_id for item in self.skills]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate skills are not allowed")
        return self


class OnboardingInfo(BaseModel):
    status: OnboardingStatusEnum
    step: int
    completed_at: datetime | None = None


class ProfileResponse(BaseModel):
    id: str
    username: str
    full_name: str
    email: str | None = None
    phone_e164: str
    country_code: str
    avatar_url: str | None = None
    date_of_birth: date | None = None
    gender: GenderEnum | None = None
    address: str | None = None
    province: str | None = None
    city: str | None = None
    bio: str | None = None
    preferred_language: LanguageEnum
    education_level: EducationEnum | None = None
    field_of_study: str | None = None
    occupation_status: OccupationEnum | None = None
    prior_business: PriorBusinessEnum | None = None
    other_skills: str | None = None
    experience_level: ProficiencyEnum | None = None
    experience_years: int | None = None
    portfolio_url: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    availability: AvailabilityEnum | None = None
    business_category: BusinessCategoryEnum | None = None
    business_model: BusinessModelEnum | None = None
    target_audience: list[TargetAudienceEnum]
    primary_goal: str | None = None
    expected_business_timeline: BusinessTimelineEnum | None = None
    available_budget_pkr: int | None = None
    available_resources: list[AvailableResourceEnum]
    team_members: int | None = None
    resource_info: list[ResourceInfoEnum]
    skills: list[ProfileSkillOut]
    onboarding: OnboardingInfo
    profile_completion: int


class UsernameAvailabilityResponse(BaseModel):
    available: bool
