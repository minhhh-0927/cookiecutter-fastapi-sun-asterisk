import logging
import time
from datetime import datetime
from uuid import uuid4

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from utilities import correlation_id

http_logger = logger.bind(name="http")
# logstash_logger = logging.getLogger('python-logstash-logger')


class HttpLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        correlation_id.set(uuid4().hex)
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        request_id = correlation_id.get()
        response.headers["x-Request-Id"] = request_id
        self.logging_dependency(request, str(process_time), response.status_code, request_id)
        return response

    def logging_dependency(self, request: Request,
                           response_time: str,
                           response_status: int,
                           request_id: str):
        message = "[{timestamp}] Req-id: {request_id} {method} {url} {status} {response_time} seconds".format(
            remote_user=request.headers["host"],
            timestamp=datetime.now(),
            request_id=request_id,
            method=request.method,
            url=request.url,
            status=response_status,
            response_time=response_time
        )
        http_logger.debug(message)
        # logstash_logger.info(message)