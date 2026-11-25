from pydantic import BaseModel

from app.schemas.common import ProficiencyEnum


class SkillCatalogItem(BaseModel):
    id: int
    slug: str
    name: str
    category: str


class ProfileSkillOut(BaseModel):
    skill_id: int
    slug: str
    name: str
    proficiency: ProficiencyEnum
