from fastapi import APIRouter
from . import admin

api_internal = APIRouter()
api_internal.include_router(admin.router)
