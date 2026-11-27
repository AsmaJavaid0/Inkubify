from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator
from supabase import Client, create_client

from app.api.deps import get_service_db
from app.api.v1.endpoints.usernames import limiter
from app.core.config import Settings, get_settings
from app.schemas.common import ApiError
from app.utils.validators import normalize_username

router = APIRouter()
_settings = get_settings()


class UsernameLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=1, max_length=72)

    @field_validator("username")
    @classmethod
    def check_username(cls, value: str) -> str:
        return normalize_username(value)


class UsernameLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


@router.post("/auth/login", response_model=UsernameLoginResponse)
@limiter.limit(_settings.RATE_LIMIT_LOGIN)
def login_with_username(
    request: Request,
    payload: UsernameLoginRequest,
    service_db: Annotated[Client, Depends(get_service_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UsernameLoginResponse:
    """Resolve username privately, then authenticate with Supabase Auth."""
    profile_result = (
        service_db.table("profiles")
        .select("id")
        .eq("username", payload.username)
        .limit(1)
        .execute()
    )
    if not profile_result.data:
        raise ApiError(status_code=401, code="unauthorized", message="Invalid username or password")

    try:
        admin_result = service_db.auth.admin.get_user_by_id(profile_result.data[0]["id"])
        auth_user = getattr(admin_result, "user", None)
        if auth_user is None:
            auth_user = getattr(getattr(admin_result, "data", None), "user", None)
        email = getattr(auth_user, "email", None)
        if not email:
            raise ValueError("Account email unavailable")

        if not settings.SUPABASE_ANON_KEY:
            raise ApiError(
                status_code=500,
                code="server_error",
                message="Supabase authentication is not configured",
            )
        auth_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        auth_result = auth_client.auth.sign_in_with_password(
            {"email": email, "password": payload.password}
        )
        session = auth_result.session
        if session is None:
            raise ValueError("Authentication session unavailable")
        return UsernameLoginResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            token_type=session.token_type,
            expires_in=session.expires_in,
        )
    except ApiError:
        raise
    except Exception as exc:
        if "email not confirmed" in str(exc).lower():
            raise ApiError(
                status_code=403,
                code="email_not_verified",
                message="Please verify your email before logging in.",
            ) from exc
        raise ApiError(
            status_code=401,
            code="unauthorized",
            message="Invalid username or password",
        ) from exc
