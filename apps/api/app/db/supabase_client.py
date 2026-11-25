from supabase import Client, create_client

from app.core.config import Settings
from app.schemas.common import ApiError


def get_user_supabase(jwt_token: str, settings: Settings) -> Client:
    """Create a Supabase client scoped to the user's JWT so RLS remains enforced."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise ApiError(
            status_code=500,
            code="server_error",
            message="Supabase client configuration is missing",
        )
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    client.postgrest.auth(jwt_token)
    return client


def get_service_supabase(settings: Settings) -> Client:
    """
    Create a Supabase service_role client.

    Used strictly for:
      1. Public username-availability boolean check (bypasses RLS safely).
      2. Server-computed protected columns (onboarding_status, onboarding_completed_at,
         profile_completion) after JWT verification and server-side validation.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ApiError(
            status_code=500,
            code="server_error",
            message="Service role configuration is missing",
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
