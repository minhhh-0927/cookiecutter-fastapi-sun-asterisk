from unittest.mock import AsyncMock

from starlette import status


class TestUserIntegration:

    def test_get_users(self, client, mocker, user_model_factory):
        async_mocker = AsyncMock(return_value=([user_model_factory], 1))
        mocker.patch(
            'components.users.repositories.UserRepositories.get_users',
            side_effect=async_mocker
        )

        response = client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["has_more"] is False
        assert data["total_count"] == 1
        assert data["data"][0]["email"] == user_model_factory.email
