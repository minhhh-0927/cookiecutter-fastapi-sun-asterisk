import asyncio

import pytest

from components.users.models import User
from components.users.repositories import UserRepositories


class TestUserRepositories:

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup(cls, db_session, user_model_factory):
        db_user = User(email=user_model_factory.email,
                       hashed_password=user_model_factory.hashed_password)
        db_session.add(db_user)
        db_session.commit()

    def test_is_user_exists_success(self, db_session, user_model_factory):
        user = asyncio.run(UserRepositories(db_session).is_user_exists(user_id=user_model_factory.id))
        assert user is True

    def test_retrieve_user_by_id_success(self, db_session, user_model_factory):
        user_actual = asyncio.run(UserRepositories(db_session).retrieve_user_by_id(user_id=user_model_factory.id))

        assert user_actual.email == user_model_factory.email
        assert user_actual.hashed_password == user_model_factory.hashed_password

    def test_get_users_success(self, db_session):
        _, total_count = asyncio.run(UserRepositories(db_session).get_users())

        assert total_count >= 1
