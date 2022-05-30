from datetime import timedelta, datetime

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from components.users.repositories import UserRepositories
from config.settings import settings
from utilities import correlation_id


async def create_access_token(data: dict) -> tuple[str, datetime]:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expires_in = datetime.utcnow() + access_token_expires
    to_encode["exp"] = expires_in
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, expires_in


async def decode_access_token(encoded_jwt: str) -> dict:
    return jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=settings.ALGORITHM)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                return self._return_unauth_res()
            if not self.__verify_jwt(request, credentials.credentials):
                return self._return_unauth_res()
            return credentials.credentials
        return self._return_unauth_res()

    async def __verify_jwt(self, request: Request, jwtoken: str) -> bool:
        token_data = await decode_access_token(jwtoken)
        if token_data["exp"] <= int(datetime.now().timestamp()):
            return False
        user = await UserRepositories(request.state.db).is_user_exists(token_data["sub"])
        if not user:
            return False
        return True

    async def _return_unauth_res(self):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(
                correlation_id=correlation_id.get(),
                err_mgs=settings.ERROR_CODE["auth"]["E1401"]["description"],
                err_code=settings.ERROR_CODE["auth"]["E1401"]["value"]
            )
        )