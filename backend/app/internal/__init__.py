from fastapi import APIRouter
from app.internal import admin
from app.core.config import Settings

def create_api_internal(settings: Settings) -> APIRouter:
    """ Complete creation of the api internal """

    # Instanciate api
    api_internal = APIRouter()

    # Include all routers
    api_internal.include_router(admin.get_router(settings))

    return api_internal
