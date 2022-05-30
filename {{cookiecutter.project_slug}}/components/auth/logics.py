from sqlalchemy.orm import Session

from components.auth.schemas import (
    LoginRequestSchema, LoginResponseSchema,
)
from components.users.repositories import UserRepositories
from config.settings import settings
from framework.dependencies.jwt_bearer import create_access_token
from framework.exceptions import NotFound, Unauthorized
from framework.hash import verify_password


class AuthLogic:

    def __init__(self, db: Session):
        self.db = db

    async def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        user = await UserRepositories(self.db).retrieve_user_by_email(email=request.email)
        if not user:
            raise NotFound(
                err_code=settings.ERROR_CODE["users"]["E0404"]["value"],
                err_msg=settings.ERROR_CODE["users"]["E0404"]["description"]
            )

        if not verify_password(request.password, user.hashed_password):
            raise Unauthorized(
                err_code=settings.ERROR_CODE["auth"]["E1400"]["value"],
                err_msg=settings.ERROR_CODE["auth"]["E1400"]["description"]
            )

        access_token, expires_in = await create_access_token({"sub": str(user.id)})
        return LoginResponseSchema(token=access_token,
                                   token_type='Bearer',
                                   expires_in=expires_in)
