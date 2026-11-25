import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.api.v1.endpoints.usernames import limiter
from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.logging import setup_logging
from app.schemas.common import ApiError

MAX_REQUEST_BYTES = 1_048_576  # 1 MB
logger = logging.getLogger("inkubify.api")


def create_app(settings_override: Settings | None = None) -> FastAPI:
    settings = settings_override or get_settings()
    setup_logging(settings.APP_ENV)

    app = FastAPI(
        title="Inkubify API",
        version=settings.VERSION,
        docs_url="/docs" if settings.APP_ENV == "development" else None,
        redoc_url=None,
    )
    app.state.limiter = limiter

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.WEB_ORIGIN],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.middleware("http")
    async def enforce_max_body_size(request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > MAX_REQUEST_BYTES:
                    err = ApiError(
                        status_code=413,
                        code="validation_error",
                        message="Request body exceeds 1 MB limit",
                    )
                    return JSONResponse(status_code=413, content=err.to_payload())
            except ValueError:
                pass
        return await call_next(request)

    @app.exception_handler(ApiError)
    async def api_error_handler(_request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=exc.to_payload())

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        fields: dict[str, str] = {}
        for err in exc.errors():
            loc = [str(part) for part in err.get("loc", []) if part not in ("body", "query")]
            key = ".".join(loc) if loc else "request"
            fields[key] = err.get("msg", "Invalid value")
        payload = ApiError(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="validation_error",
            message="Validation failed",
            fields=fields,
        ).to_payload()
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=payload,
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(_request: Request, _exc: RateLimitExceeded) -> JSONResponse:
        payload = ApiError(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="rate_limited",
            message="Too many requests, please try again in a minute",
        ).to_payload()
        return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled API exception: %s", type(exc).__name__)
        payload = ApiError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="server_error",
            message="An unexpected server error occurred",
        ).to_payload()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=payload,
        )

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
