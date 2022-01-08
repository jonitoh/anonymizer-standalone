from fastapi import APIRouter
from app.routers import datasets, statistics
from app.core.config import Settings

def create_api_router(settings: Settings) -> APIRouter:
    """ Complete creation of the api router """

    # Instanciate api
    api_router = APIRouter()

    # Include all routers
    api_router.include_router(datasets.get_router(settings))
    api_router.include_router(statistics.get_router(settings))    

    return api_router