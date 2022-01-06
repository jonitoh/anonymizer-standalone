import os
from urllib.parse import quote_plus

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from .dependencies import get_query_token, get_token_header

from .internal import api_internal
from .routers import api_router

ORIGINS = [
    "http://0.0.0.0:3000",
    "http://localhost:3000"
]
PROJECT_NAME = "Anonymizer standalone"
API_VERSION_URL = "/v1"

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url=f"{API_VERSION_URL}/openapi.json",
)#(dependencies=[Depends(get_query_token)])

if ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=API_VERSION_URL)
app.include_router(api_internal, prefix=API_VERSION_URL)

mongo_client = None

def get_client():
    """
    Setup a mongo client for the site
    :return:
    """
    global mongo_client
    if bool(mongo_client):
        return mongo_client
    host = os.getenv('MONGODB_HOST', '')
    username = os.getenv('MONGODB_USER', '')
    password = os.getenv('MONGODB_PASSWORD', '')
    port = int(os.getenv('MONGODB_PORT', 27017))
    endpoint = 'mongodb://{0}:{1}@{2}'.format(quote_plus(username),
                                              quote_plus(password), host)
    mongo_client = MongoClient(endpoint, port)
    return mongo_client

@app.get('/')
async def root():
    return {'message': 'Hello World'}
