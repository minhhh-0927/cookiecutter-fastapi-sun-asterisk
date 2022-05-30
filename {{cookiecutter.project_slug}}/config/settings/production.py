from fastapi import FastAPI, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from config.settings.base import *
from framework.dependencies.basic_auth import check_basic_auth
from framework.logger import init_logging_elk_stack
from framework.middlewares.sentry import SentryMiddleware


def get_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        dependencies=Depends(check_basic_auth)
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[settings.ALLOWED_HOSTS]
    )
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(SentryMiddleware)
    app.add_event_handler("startup", init_logging_elk_stack)
    return app
