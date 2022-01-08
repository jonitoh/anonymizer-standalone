"""Main entry point of the application"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from app.core.config import get_settings
from app.internal import create_api_internal
from app.routers import create_api_router

mongo_client = None

def get_client(uri: str):
    """
    Setup a mongo client for the site
    :return:
    """
    global mongo_client
    if bool(mongo_client):
        return mongo_client
    return MongoClient(uri)

def create_app() -> FastAPI:
    """ Complete creation of the app """
    global mongo_client # TODO: to remove; too messy
    # Instanciate settings
    settings = get_settings()

    # Instanciate database
    mongo_client = get_client(settings.MONGO_DATABASE_URI)

    # Instanciate app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=settings.OPENAPI_URL,
        debug=settings.DEBUG,
    )

    # C.O.R.S 
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add static folder
    app.mount(settings.STATIC_FOLDER, StaticFiles(directory="static"), name="static")

    # Include all routers
    app.include_router(create_api_router(settings), prefix=settings.API_VERSION_URL)

    # Include all internals
    app.include_router(create_api_internal(settings), prefix=settings.API_VERSION_URL)


    # HELLO WORLD ROUTE
    @app.get('/hello-world')
    def test_route():
        return {'message': 'Hello World'}

    # ROOT ROUTE
    @app.get("/", include_in_schema=False)
    def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse("/docs")

    """@app.on_event("startup")
    async def connect_to_database() -> None:
        database = _get_database()
        if not database.is_connected:
            await database.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        database = _get_database()
        if database.is_connected:
            await database.disconnect()"""

    return app

app = create_app()
