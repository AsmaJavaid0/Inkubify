from dataclasses import dataclass
from functools import lru_cache

import jwt
from jwt import PyJWKClient, PyJWTError

from app.core.config import Settings
from app.schemas.common import ApiError


@dataclass(frozen=True)
class AuthenticatedUser:
    id: str
    email: str | None
    token: str


@lru_cache(maxsize=4)
def _get_jwk_client(jwks_url: str) -> PyJWKClient:
    return PyJWKClient(jwks_url, cache_keys=True, lifespan=300)


def verify_supabase_jwt(token: str, settings: Settings) -> AuthenticatedUser:
    """Verify a Supabase access token via JWKS (ES256/RS256) or HS256 secret."""
    if not token:
        raise ApiError(status_code=401, code="unauthorized", message="Missing access token")

    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg", "")

        if alg == "HS256":
            if not settings.SUPABASE_JWT_SECRET:
                raise ApiError(
                    status_code=401,
                    code="unauthorized",
                    message="Token algorithm not configured",
                )
            claims = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
                issuer=settings.jwt_issuer,
            )
        elif alg in ("ES256", "RS256", "EdDSA"):
            jwk_client = _get_jwk_client(settings.jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=[alg],
                audience="authenticated",
                issuer=settings.jwt_issuer,
            )
        else:
            raise ApiError(
                status_code=401,
                code="unauthorized",
                message="Unsupported token algorithm",
            )
    except ApiError:
        raise
    except PyJWTError as exc:
        raise ApiError(
            status_code=401,
            code="unauthorized",
            message="Invalid or expired access token",
        ) from exc
    except Exception as exc:
        raise ApiError(
            status_code=401,
            code="unauthorized",
            message="Could not verify access token",
        ) from exc

    sub = claims.get("sub")
    if not sub or not isinstance(sub, str):
        raise ApiError(
            status_code=401,
            code="unauthorized",
            message="Token missing subject claim",
        )

    email = claims.get("email")
    return AuthenticatedUser(
        id=sub,
        email=email if isinstance(email, str) else None,
        token=token,
    )
