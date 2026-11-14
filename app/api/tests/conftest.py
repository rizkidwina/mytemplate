import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from api.dependencies import get_db
from core.security import get_current_user_id
from db.base import Base
from features.products import models as product_models  # noqa: F401
from features.users import models as user_models  # noqa: F401
from main import app

TEST_AUTH_USER_ID = "test-auth-user-001"


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine, None, None]:
    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "TEST_DATABASE_URL is not configured. Please configure it in your .env file."
        )

    if not database_url.endswith("/app_test"):
        raise RuntimeError("Tests must use the dedicated app_test database.")

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine: Engine) -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
        autoflush=False,
        expire_on_commit=False,
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    def override_get_current_user_id() -> str:
        return TEST_AUTH_USER_ID

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
