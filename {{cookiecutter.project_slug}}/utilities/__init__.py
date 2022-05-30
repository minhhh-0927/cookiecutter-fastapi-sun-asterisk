import os
from contextvars import ContextVar
from functools import lru_cache
from typing import Optional

correlation_id: ContextVar[Optional[str]] = ContextVar(
    'correlation_id', default=None
)


@lru_cache()
def get_db_url():
    # sourcery skip: assign-if-exp, or-if-exp-identity, reintroduce-else, use-fstring-for-formatting
    if os.getenv("DATABASE_URI"):
        return os.getenv("DATABASE_URI")

    return "{}://{}:{}@{}:{}/{}".format(
        os.getenv("DB_ENGINE"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
    )
