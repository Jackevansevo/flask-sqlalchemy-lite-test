import pytest
from app import create_app

from sqlalchemy_utils import create_database, drop_database
from app import db, Model


@pytest.fixture
def app_ctx(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture(scope="session", autouse=True)
def _manage_test_database():
    app = create_app(
        {"SQLALCHEMY_ENGINES": {"default": "postgresql+psycopg:///testdb"}}
    )

    with app.app_context():
        engines = db.engines

    for engine in engines.values():
        create_database(engine.url)

    Model.metadata.create_all(engines["default"])

    yield

    for engine in engines.values():
        drop_database(engine.url)


@pytest.fixture
def app():
    app = create_app(
        {"SQLALCHEMY_ENGINES": {"default": "postgresql+psycopg:///testdb"}}
    )

    with app.app_context():
        engines = db.engines

    cleanup = []

    for key, engine in engines.items():
        connection = engine.connect()
        transaction = connection.begin()
        engines[key] = connection
        cleanup.append((key, engine, connection, transaction))

    yield app

    for key, engine, connection, transaction in cleanup:
        transaction.rollback()
        connection.close()
        engines[key] = engine
