from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import os
from urllib.parse import quote_plus


app = FastAPI()
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