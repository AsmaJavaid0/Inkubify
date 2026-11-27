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


class AvailabilityEnum(StrEnum):
    full_time = "full_time"
    part_time = "part_time"
    evenings_weekends = "evenings_weekends"
    flexible = "flexible"


class BusinessCategoryEnum(StrEnum):
    ecommerce = "ecommerce"
    technology_based = "technology_based"


class BusinessModelEnum(StrEnum):
    b2b = "b2b"
    d2c = "d2c"
    dropshipping = "dropshipping"
    b2c = "b2c"


class BusinessTimelineEnum(StrEnum):
    within_3_months = "within_3_months"
    three_to_six_months = "3_6_months"
    six_to_twelve_months = "6_12_months"
    one_to_two_years = "1_2_years"
    exploring = "exploring"


class TargetAudienceEnum(StrEnum):
    individual_consumers = "individual_consumers"
    small_businesses = "small_businesses"
    startups = "startups"
    enterprises = "enterprises"
    students = "students"
    professionals = "professionals"
    government = "government"
    nonprofits = "nonprofits"


class AvailableResourceEnum(StrEnum):
    laptop_computer = "laptop_computer"
    internet = "internet"
    workspace = "workspace"
    equipment = "equipment"
    inventory = "inventory"
    supplier_network = "supplier_network"
    transport = "transport"
    team = "team"
    other = "other"


class ResourceInfoEnum(StrEnum):
    personal_savings = "personal_savings"
    family_support = "family_support"
    bank_loan = "bank_loan"
    investor_funding = "investor_funding"
    grant = "grant"
    incubator_support = "incubator_support"
    other = "other"
