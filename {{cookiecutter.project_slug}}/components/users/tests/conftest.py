from faker import Faker

from config.conftest import *
from components.users.models import User


@pytest.fixture(scope="session")
def user_model_factory(db_session):
    user_factory = Faker()
    user_email = user_factory.email()
    hashed_password = user_factory.sentence().strip()

    return User(email=user_email,
                id=1,
                hashed_password=hashed_password,
                is_active=True)
