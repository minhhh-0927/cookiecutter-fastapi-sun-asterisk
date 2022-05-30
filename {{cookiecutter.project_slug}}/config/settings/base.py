import os
import pathlib
from functools import lru_cache
from typing import Optional, List, Union

import yaml
from dotenv import load_dotenv
from fastapi import Request
from pydantic import BaseSettings, Field, validator, AnyHttpUrl
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utilities import get_db_url

BASE_DIR = f"{pathlib.Path(__file__).parent.parent.parent.resolve()}"

# Load ENV from file .env
load_dotenv(dotenv_path=f"{BASE_DIR}/.env")

# Constants config yaml
ERROR_CODE_FILE_CONF = f"{BASE_DIR}/config/constants/error_code.yml"
COMPONENTS_MSG_FILE_CONF = f"{BASE_DIR}/config/constants/components_msg.yml"

# Upload folder config
UPLOAD_FOLDER = f"{BASE_DIR}/upload"

# SQLAlchemy
SQLALCHEMY_DATABASE_URL = get_db_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@lru_cache()
def read_thresh_yaml(yaml_file: str) -> dict:
    with open(yaml_file) as f:
        return yaml.safe_load(f)


class Settings(BaseSettings):
    PROJECT_NAME: Optional[str] = "{{ cookiecutter.project_slug }}"
    ENV: str = os.getenv("ENV")
    TIME_ZONE: str = "Asia/Ho_Chi_Minh"
    BASE_DIR: str = BASE_DIR
    LANGUAGE_CODE: str = "en-us"
    DEBUG: bool = True

    ERROR_CODE: dict = read_thresh_yaml(ERROR_CODE_FILE_CONF)
    SCORING_LOGIC_CONFIG: dict = read_thresh_yaml(COMPONENTS_MSG_FILE_CONF)

    DECLARATIVE_BASE = declarative_base()

    UPLOAD_FOLDER: str = UPLOAD_FOLDER

    # AWS credentials
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME: Optional[str] = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME: Optional[str] = os.getenv("AWS_S3_REGION_NAME")
    AWS_VIDEO_LOCATION: Optional[str] = os.getenv("AWS_VIDEO_LOCATION")

    # Authentication
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pagination
    DEFAULT_LIMIT: int = 10
    DEFAULT_OFFSET: int = 0

    # CORS
    CORS_ALLOWED_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(..., env="CORS_ALLOWED_ORIGINS")

    @validator("CORS_ALLOWED_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    # CORS
    ALLOWED_HOSTS: Union[str, List[AnyHttpUrl]] = Field(..., env="ALLOWED_HOST")

    @validator("ALLOWED_HOSTS", pre=True)
    def _assemble_allowed_hosts(cls, allowed_hosts):
        if isinstance(allowed_hosts, str):
            return [item.strip() for item in allowed_hosts.split(",")]
        return allowed_hosts

    # Worker
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND")

    # Redis cache
    REDIS_URL: str = os.getenv("REDIS_URL")


@lru_cache()
def get_settings():
    return Settings()


def get_db(request: Request):
    return request.state.db


settings = get_settings()
