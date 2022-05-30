import os

import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


def init_cache():
    redis = aioredis.from_url(os.getenv("REDIS_URL"),
                              encoding="utf8",
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-{{ cookiecutter.project_slug }}-cache")
