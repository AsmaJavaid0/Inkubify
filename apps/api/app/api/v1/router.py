from fastapi import APIRouter

from app.api.v1.endpoints import catalog, health, profiles, usernames

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(usernames.router, tags=["usernames"])
api_router.include_router(catalog.router, tags=["catalog"])
api_router.include_router(profiles.router, tags=["profiles"])
