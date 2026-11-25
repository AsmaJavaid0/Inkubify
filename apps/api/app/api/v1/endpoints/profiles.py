from typing import Annotated

from fastapi import APIRouter, Depends
from supabase import Client

from app.api.deps import get_current_user, get_service_db, get_user_db
from app.core.security import AuthenticatedUser
from app.schemas.profile import (
    ProfilePatchRequest,
    ProfileResponse,
    ProfileSkillsPutRequest,
)
from app.services.profile_service import (
    complete_my_onboarding,
    get_my_profile,
    patch_my_profile,
    replace_my_skills,
)

router = APIRouter()


@router.get("/profiles/me", response_model=ProfileResponse)
def read_my_profile(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    user_db: Annotated[Client, Depends(get_user_db)],
) -> ProfileResponse:
    return get_my_profile(user_db, user)


@router.patch("/profiles/me", response_model=ProfileResponse)
def update_my_profile(
    payload: ProfilePatchRequest,
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    user_db: Annotated[Client, Depends(get_user_db)],
    service_db: Annotated[Client, Depends(get_service_db)],
) -> ProfileResponse:
    return patch_my_profile(user_db, service_db, user, payload)


@router.put("/profiles/me/skills", response_model=ProfileResponse)
def update_my_skills(
    payload: ProfileSkillsPutRequest,
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    user_db: Annotated[Client, Depends(get_user_db)],
    service_db: Annotated[Client, Depends(get_service_db)],
) -> ProfileResponse:
    return replace_my_skills(user_db, service_db, user, payload)


@router.post("/profiles/me/onboarding/complete", response_model=ProfileResponse)
def finish_onboarding(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    user_db: Annotated[Client, Depends(get_user_db)],
    service_db: Annotated[Client, Depends(get_service_db)],
) -> ProfileResponse:
    return complete_my_onboarding(user_db, service_db, user)
