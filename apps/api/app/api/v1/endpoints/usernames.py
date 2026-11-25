from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from supabase import Client

from app.api.deps import get_service_db
from app.core.config import get_settings
from app.schemas.common import ApiError
from app.schemas.profile import UsernameAvailabilityResponse
from app.utils.validators import normalize_username

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
_settings = get_settings()


@router.get("/usernames/availability", response_model=UsernameAvailabilityResponse)
@limiter.limit(_settings.RATE_LIMIT_USERNAME_CHECK)
def check_username_availability(
    request: Request,
    service_db: Annotated[Client, Depends(get_service_db)],
    username: str = Query(..., min_length=1, max_length=32),
) -> UsernameAvailabilityResponse:
    try:
        cleaned = normalize_username(username)
    except ValueError as exc:
        raise ApiError(
            status_code=422,
            code="validation_error",
            message=str(exc),
            fields={"username": str(exc)},
        ) from exc

    res = (
        service_db.table("profiles")
        .select("id")
        .eq("username", cleaned)
        .limit(1)
        .execute()
    )
    return UsernameAvailabilityResponse(available=len(res.data or []) == 0)
