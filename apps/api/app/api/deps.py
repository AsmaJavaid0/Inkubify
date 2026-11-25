from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

from app.core.config import Settings, get_settings
from app.core.security import AuthenticatedUser, verify_supabase_jwt
from app.db.supabase_client import get_service_supabase, get_user_supabase
from app.schemas.common import ApiError

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthenticatedUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise ApiError(
            status_code=401,
            code="unauthorized",
            message="Missing Bearer authorization token",
        )
    return verify_supabase_jwt(credentials.credentials, settings)


def get_user_db(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Client:
    return get_user_supabase(user.token, settings)


def get_service_db(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Client:
    return get_service_supabase(settings)
