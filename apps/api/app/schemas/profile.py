from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.catalog import ProfileSkillOut
from app.schemas.common import (
    EducationEnum,
    GenderEnum,
    InterestEnum,
    LanguageEnum,
    OccupationEnum,
    OnboardingStatusEnum,
    PrimaryGoalEnum,
    PriorBusinessEnum,
    ProficiencyEnum,
    WeeklyHoursEnum,
    WorkExperienceEnum,
)
from app.utils.validators import (
    normalize_full_name,
    normalize_instagram_url,
    validate_date_of_birth,
    validate_linkedin_url,
    validate_province_and_city,
)


class ProfilePatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = None
    avatar_url: str | None = None
    date_of_birth: date | None = None
    gender: GenderEnum | None = None
    province: str | None = None
    city: str | None = None
    bio: str | None = None
    preferred_language: LanguageEnum | None = None

    education_level: EducationEnum | None = None
    field_of_study: str | None = None
    occupation_status: OccupationEnum | None = None
    work_experience: WorkExperienceEnum | None = None
    prior_business: PriorBusinessEnum | None = None

    primary_goal: PrimaryGoalEnum | None = None
    weekly_hours: WeeklyHoursEnum | None = None
    interested_in: list[InterestEnum] | None = None
    instagram_url: str | None = None
    linkedin_url: str | None = None

    onboarding_step: int | None = Field(default=None, ge=1, le=5)

    @field_validator("full_name")
    @classmethod
    def check_full_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return normalize_full_name(v)

    @field_validator("avatar_url")
    @classmethod
    def check_avatar_url(cls, v: str | None) -> str | None:
        if v is None:
            return None
        cleaned = v.strip()
        if not cleaned:
            return None
        if not cleaned.startswith(("https://", "http://")):
            raise ValueError("Avatar URL must be an http(s) URL")
        if len(cleaned) > 500:
            raise ValueError("Avatar URL is too long")
        return cleaned

    @field_validator("date_of_birth")
    @classmethod
    def check_dob(cls, v: date | None) -> date | None:
        if v is None:
            return None
        return validate_date_of_birth(v)

    @field_validator("bio")
    @classmethod
    def check_bio(cls, v: str | None) -> str | None:
        if v is None:
            return None
        cleaned = v.strip()
        if not cleaned:
            return None
        if len(cleaned) > 280:
            raise ValueError("Bio must be 280 characters or fewer")
        return cleaned

    @field_validator("field_of_study")
    @classmethod
    def check_field_of_study(cls, v: str | None) -> str | None:
        if v is None:
            return None
        cleaned = v.strip()
        if not cleaned:
            return None
        if not (2 <= len(cleaned) <= 80):
            raise ValueError("Field of study must be between 2 and 80 characters")
        return cleaned

    @field_validator("interested_in")
    @classmethod
    def check_interested_in(cls, v: list[InterestEnum] | None) -> list[InterestEnum] | None:
        if v is None:
            return None
        # Deduplicate while preserving order
        return list(dict.fromkeys(v))

    @field_validator("instagram_url")
    @classmethod
    def check_instagram(cls, v: str | None) -> str | None:
        return normalize_instagram_url(v)

    @field_validator("linkedin_url")
    @classmethod
    def check_linkedin(cls, v: str | None) -> str | None:
        return validate_linkedin_url(v)

    @model_validator(mode="after")
    def check_location(self) -> "ProfilePatchRequest":
        prov, city = validate_province_and_city(self.province, self.city)
        if "province" in self.model_fields_set:
            self.province = prov
        if "city" in self.model_fields_set:
            self.city = city
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
    province: str | None = None
    city: str | None = None
    bio: str | None = None
    preferred_language: LanguageEnum
    education_level: EducationEnum | None = None
    field_of_study: str | None = None
    occupation_status: OccupationEnum | None = None
    work_experience: WorkExperienceEnum | None = None
    prior_business: PriorBusinessEnum | None = None
    primary_goal: PrimaryGoalEnum | None = None
    weekly_hours: WeeklyHoursEnum | None = None
    interested_in: list[InterestEnum]
    instagram_url: str | None = None
    linkedin_url: str | None = None
    skills: list[ProfileSkillOut]
    onboarding: OnboardingInfo
    profile_completion: int


class UsernameAvailabilityResponse(BaseModel):
    available: bool
