from fastapi import status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utilities import correlation_id


class BaseException(Exception):
    def __init__(self,
                 err_code: int,
                 err_msg: str):
        self.err_code = err_code
        self.err_msg = err_msg


class BadRequest(BaseException):
    def __init__(self, err_code, err_msg):
        super(BadRequest, self).__init__(err_code, err_msg)
        self.status_code = status.HTTP_400_BAD_REQUEST


class Unauthorized(BaseException):
    def __init__(self, err_code, err_msg):
        super(Unauthorized, self).__init__(err_code, err_msg)
        self.status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(BaseException):
    def __init__(self, err_code, err_msg):
        super(PermissionDenied, self).__init__(err_code, err_msg)
        self.status_code = status.HTTP_403_FORBIDDEN


class NotFound(BaseException):
    def __init__(self, err_code, err_msg):
        super(NotFound, self).__init__(err_code, err_msg)
        self.status_code = status.HTTP_404_NOT_FOUND


class UnprocessableEntity(BaseException):
    def __init__(self, err_code, err_msg):
        super(UnprocessableEntity, self).__init__(err_code, err_msg)
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class InternalServerError(BaseException):
    def __init__(self, err_code, err_msg):
        super(InternalServerError, self).__init__(err_code, err_msg)
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


async def unicorn_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=dict(
            correlation_id=correlation_id.get(),
            err_msg=exc.errors(),
            err_code="ECC203"  # This is example
        )
    )
