"""Importation of all external settings or configurations to smoothly run the application"""
import os
from pathlib import Path
from functools import lru_cache
from typing import Union, List, Any, Dict, Optional

from pydantic import BaseSettings, SecretStr, AnyHttpUrl, AnyUrl, validator

from ..utils import parse_list


class Settings(BaseSettings):

    # DATABASE
    MONGO_USER: str = None
    MONGO_PASSWORD: SecretStr = None
    MONGO_HOST: str = None
    MONGO_PORT: int = 27017
    MONGO_URI_OPTIONS: str = None
    MONGO_DATABASE_URI: Optional[AnyUrl] = None

    @validator("MONGO_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, uri: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(uri, str):
            return uri
        formed_uri = f"mongodb://{values.get('MONGO_USER')}:{values.get('MONGO_PASSWORD')}@{values.get('MONGO_HOST')}"
        port = values.get('MONGO_PORT', None)
        if port:
            formed_uri += f":{port}"
        options = values.get('MONGO_URI_OPTIONS', None)
        if options:
            formed_uri += options
        return formed_uri

    DATABASE_NAME: str
    COLLECTION_DATASET_NAME: str
    COLLECTION_METADATA_NAME: str

    # APP CONFIGURATION -- BASICS
    PROJECT_NAME: str
    API_VERSION: str
    API_VERSION_URL:str
    OPENAPI_URL: str = None

    @validator("OPENAPI_URL", pre=True)
    def assemble_openapi_url(cls, url: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(url, str):
            return url
        return f"{values.get('API_VERSION_URL')}/openapi.json"

    STATIC_FOLDER: str = "/static"
    AUT_KEY: str = None
    API_KEY: str = None

    DEBUG: bool = False
    SECRET_KEY: SecretStr = "secret_key"
    CORS_ORIGINS: Union[str, List[AnyHttpUrl], List[str]] = ["http://0.0.0.0:3000", "http://localhost:3000"]
    # TODO: fix CORS_ORIGINS
    # @validator("CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, cors_origins: Optional[str]):
    #     print("assemble cors origins for", cors_origins)
    #     parser = parse_list(
    #         class_type=AnyHttpUrl,
    #         default=['*'],
    #         separator=",",
    #         raise_error=False
    #     )
    #     return parser(cors_origins)
    
    # APP CONFIGURATION -- DATASETS
    TOO_LARGE_FILE_SIZE: int
    UPLOAD_FOLDER: str = "/upload"
    DATETIME_FORMAT_FOR_UPLOAD: str = "%Y-%m-%d-%H-%M"
    DEFAULT_MEDIA_TYPE: str = "application/octet-stream"



    class Config:
        #env_nested_delimiter = '__'
        case_sensitive = False
        env_file = os.getenv("ENVIRONMENT_FILE", 'backend.env')
        env_file_encoding = 'utf-8'
        #env_prefix = ""
        #secrets_dir = "./secrets"

settings = Settings()

@lru_cache()
def get_settings():
    """ cf. https://fastapi.tiangolo.com/advanced/settings/"""
    return Settings()
