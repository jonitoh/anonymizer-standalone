from fastapi import APIRouter
from . import datasets, statistics

api_router = APIRouter()
api_router.include_router(datasets.router)
api_router.include_router(statistics.router)