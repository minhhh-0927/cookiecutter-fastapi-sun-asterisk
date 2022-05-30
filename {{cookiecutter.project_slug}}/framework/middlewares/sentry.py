import sentry_sdk
from fastapi import Request, status
from loguru import logger

from starlette.middleware.base import BaseHTTPMiddleware

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",

)
from starlette.responses import JSONResponse


class SentryMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=dict(
                err_mgs="Unknown error",
                err_code="E0300"
            )
        )
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(e)
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                scope.user = {
                    "ip_address": request.client.host,
                }
                sentry_sdk.capture_exception(e)
            raise e

        return response
