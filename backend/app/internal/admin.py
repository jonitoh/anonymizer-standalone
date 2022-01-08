from fastapi import APIRouter
from app.core.config import Settings

def get_router(settings: Settings) -> APIRouter:
    router = APIRouter(
        prefix="/admin",
        tags=["admin"],
        responses={418: {"description": "I'm a teapot"}},
    )


    @router.post("/")
    async def update_admin():
        return {"message": "Admin getting schwifty"}
    
    return router

