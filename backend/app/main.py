import os
from urllib.parse import quote_plus

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from .dependencies import get_query_token, get_token_header

from .internal import admin
from .routers import datasets, statistics

origins = [
    "http://0.0.0.0:3000",
    "http://localhost:3000"
]
app = FastAPI()#(dependencies=[Depends(get_query_token)])
app.include_router(datasets.router)
app.include_router(statistics.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[],#Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
