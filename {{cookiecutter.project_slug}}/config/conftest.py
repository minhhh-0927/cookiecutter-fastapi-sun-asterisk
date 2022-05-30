import alembic
import pytest
from alembic.config import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from starlette.testclient import TestClient

from config.settings.base import engine

Base = declarative_base()


@pytest.fixture(scope="session")
def connection():
    return engine.connect()


@pytest.fixture(scope="session")
def db_session(setup_database, connection):
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def client(apply_migrations: None):
    from config.app import app
    with TestClient(app) as c:
        yield c
