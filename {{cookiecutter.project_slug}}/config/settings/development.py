from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from config.settings.base import *


def get_app() -> FastAPI:
    app = FastAPI()
    app.mount("/upload", StaticFiles(directory="upload"), name="upload")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="The docs api of {{ cookiecutter.project_slug }} project",
            version="2.5.0",
            description="This is a very custom OpenAPI schema",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app
