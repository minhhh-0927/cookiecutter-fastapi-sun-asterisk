from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from components.auth.routers import router as auth_router
from components.healthy_check.routers import router as healthy_check_router
from components.users.routers import router as users_router
from components.uploads.routers import router as uploads_router

from config.settings import get_app, settings
from framework.cache import init_cache
from framework.exceptions import unicorn_exception_handler
from framework.logger import init_logging_loguru
from framework.middlewares.db_session import DbSessionMiddleware
from framework.middlewares.http_logging import HttpLoggingMiddleware

app = get_app()

# Add middlewares
app.add_middleware(DbSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HttpLoggingMiddleware, some_attribute="some_attribute")

# Add exceptions
app.add_exception_handler(RequestValidationError, handler=unicorn_exception_handler)

# Add routers
app.include_router(users_router)
app.include_router(healthy_check_router)
app.include_router(auth_router)
app.include_router(uploads_router)

# Add event
app.add_event_handler("startup", init_logging_loguru)
app.add_event_handler("startup", init_cache)

