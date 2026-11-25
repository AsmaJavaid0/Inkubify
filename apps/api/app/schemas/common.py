from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    fields: dict[str, str] | None = None


class ErrorEnvelope(BaseModel):
    error: ErrorDetail


class ApiError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        fields: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.fields = fields

    def to_payload(self) -> dict[str, Any]:
        detail = ErrorDetail(code=self.code, message=self.message, fields=self.fields)
        return ErrorEnvelope(error=detail).model_dump(exclude_none=True)


class GenderEnum(StrEnum):
    female = "female"
    male = "male"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class LanguageEnum(StrEnum):
    en = "en"
    ur = "ur"


class EducationEnum(StrEnum):
    matric_olevels = "matric_olevels"
    intermediate_alevels = "intermediate_alevels"
    diploma = "diploma"
    bachelors = "bachelors"
    masters = "masters"
    phd = "phd"
    other = "other"


class OccupationEnum(StrEnum):
    student = "student"
    employed = "employed"
    self_employed = "self_employed"
    freelancer = "freelancer"
    unemployed = "unemployed"
    other = "other"


class WorkExperienceEnum(StrEnum):
    none = "none"
    lt_1 = "lt_1"
    one_to_three = "1_3"
    three_to_five = "3_5"
    five_plus = "5_plus"


class PriorBusinessEnum(StrEnum):
    none = "none"
    tried_before = "tried_before"
    running_now = "running_now"


class PrimaryGoalEnum(StrEnum):
    side_income = "side_income"
    full_time_business = "full_time_business"
    scale_existing = "scale_existing"
    explore_learn = "explore_learn"


class WeeklyHoursEnum(StrEnum):
    lt_5 = "lt_5"
    five_to_ten = "5_10"
    ten_to_twenty = "10_20"
    twenty_to_forty = "20_40"
    forty_plus = "40_plus"


class ProficiencyEnum(StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class OnboardingStatusEnum(StrEnum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class InterestEnum(StrEnum):
    ecommerce = "ecommerce"
    tech_services = "tech_services"
