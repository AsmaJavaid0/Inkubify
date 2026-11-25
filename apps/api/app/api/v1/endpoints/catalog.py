from typing import Annotated

from fastapi import APIRouter, Depends
from supabase import Client

from app.api.deps import get_current_user, get_user_db
from app.core.security import AuthenticatedUser
from app.schemas.catalog import SkillCatalogItem
from app.services.profile_service import list_active_skills

router = APIRouter()


@router.get("/catalog/skills", response_model=list[SkillCatalogItem])
def get_skills_catalog(
    _user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    user_db: Annotated[Client, Depends(get_user_db)],
) -> list[SkillCatalogItem]:
    return list_active_skills(user_db)
