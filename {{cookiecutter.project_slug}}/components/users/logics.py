from sqlalchemy.orm import Session

from components.users.repositories import UserRepositories
from components.users.schemas import (
    UserGetRequestSchema, UserGetResponseSchema,
    UsersGetRequestSchema, UsersGetResponseSchema,
    UserCreateRequestSchema, UserCreateResponseSchema,
    UserUpdateRequestSchema, UserUpdateResponseSchema
)
from config.settings import settings
from framework.exceptions import NotFound
from framework.hash import get_password_hash


class UserLogic:

    def __init__(self, db: Session):
        self.db = db

    async def retrieve_user(self, request: UserGetRequestSchema) -> UserGetResponseSchema:
        user = await UserRepositories(self.db).retrieve_user_by_id(user_id=request.user_id)
        if not user:
            raise NotFound(
                err_code=settings.ERROR_CODE["users"]["E0404"]["value"],
                err_msg=settings.ERROR_CODE["users"]["E0404"]["description"]
            )
        return UserGetResponseSchema.from_orm(user)

    async def get_users(self, request: UsersGetRequestSchema) -> UsersGetResponseSchema:
        users, total_count = await UserRepositories(self.db).get_users(user_id=request.user_id,
                                                                      email=request.email,
                                                                      limit=request.limit,
                                                                      offset=request.offset)
        data = [
            dict(
                email=item.email,
                id=item.id,
                is_active=item.is_active,
            )
            for item in users
        ]
        return UsersGetResponseSchema(data=data, total_count=total_count)

    async def create_user(self, request: UserCreateRequestSchema) -> UserCreateResponseSchema:
        hash_password = get_password_hash(request.password)
        user = await UserRepositories(self.db).create_user(email=request.email,
                                                          password=hash_password)
        return UserCreateResponseSchema.from_orm(user)

    async def update_user(self, request: UserUpdateRequestSchema) -> UserUpdateResponseSchema:
        user_exist = await UserRepositories(self.db).is_user_exists(user_id=request.user_id)
        if not user_exist:
            raise NotFound(
                err_code=settings.ERROR_CODE["users"]["E0404"]["value"],
                err_msg=settings.ERROR_CODE["users"]["E0404"]["description"]
            )

        hash_password = get_password_hash(request.password) if request.password else None
        await UserRepositories(self.db).update_user(
            user_id=request.user_id,
            email=request.email,
            password=hash_password
        )
        user = await UserRepositories(self.db).retrieve_user_by_id(user_id=request.user_id)
        return UserUpdateResponseSchema.from_orm(user)
