import sqlalchemy
from fastapi import Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from config.settings import SessionLocal


class DbSessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=dict(
                    err_mgs="Unknown error",
                    err_code="E0300"
                )
            )
        try:
            request.state.db = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response
