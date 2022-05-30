import asyncio
from unittest.mock import AsyncMock

from components.users.logics import UserLogic
from components.users.schemas import (
    UserGetRequestSchema, UserGetResponseSchema,
    UsersGetRequestSchema, UsersGetResponseSchema
)
from config.settings import settings


class TestUserLogic:

    def test_retrieve_user_success(self, db_session, mocker, user_model_factory):
        async_mocker = AsyncMock(return_value=user_model_factory)
        mocker.patch(
            'components.users.repositories.UserRepositories.retrieve_user_by_id',
            side_effect=async_mocker
        )

        request_schema = UserGetRequestSchema(user_id=user_model_factory.id)
        user_actual = asyncio.run(UserLogic(db_session).retrieve_user(request_schema))

        assert isinstance(user_actual, UserGetResponseSchema)
        assert user_actual.email == user_model_factory.email
        assert int(user_actual.id) == user_model_factory.id

    def test_get_users(self, db_session, mocker, user_model_factory):
        async_mocker = AsyncMock(return_value=([user_model_factory], 1))
        mocker.patch(
            'components.users.repositories.UserRepositories.get_users',
            side_effect=async_mocker
        )

        request_schema = UsersGetRequestSchema(limit=settings.DEFAULT_LIMIT,
                                               offset=settings.DEFAULT_OFFSET)
        users_actual = asyncio.run(UserLogic(db_session).get_users(request_schema))

        assert isinstance(users_actual, UsersGetResponseSchema)
        assert int(users_actual.total_count) == 1
        assert users_actual.has_more is None
        assert users_actual.data[0].email == user_model_factory.email
