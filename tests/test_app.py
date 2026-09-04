from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from databases import Database
from sqlalchemy import create_engine

from src.api.database.db import metadata
from src.api.schemas.auth import LoginRequest, SignUpRequest
from src.api.services.auth import AuthServiceImpl


@pytest.fixture
async def auth_service():
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test_users.db"
        temp_db = Database(f"sqlite:///{db_path}")
        test_engine = create_engine(f"sqlite:///{db_path}")
        metadata.create_all(test_engine)

        service = AuthServiceImpl()
        service.db = temp_db

        await temp_db.connect()
        try:
            yield service
        finally:
            await temp_db.disconnect()
            test_engine.dispose()


@pytest.mark.asyncio
async def test_signup_creates_user(auth_service):
    user = await auth_service.signup(SignUpRequest(username="alice", password="secret123"))
    assert user["username"] == "alice"
    assert user["password"] != "secret123"


@pytest.mark.asyncio
async def test_signup_duplicate_username_raises(auth_service):
    await auth_service.signup(SignUpRequest(username="bob", password="secret123"))
    with pytest.raises(ValueError):
        await auth_service.signup(SignUpRequest(username="bob", password="other123"))


@pytest.mark.asyncio
async def test_login_success_and_failure(auth_service):
    await auth_service.signup(SignUpRequest(username="carol", password="secret123"))

    ok = await auth_service.login(LoginRequest(username="carol", password="secret123"))
    assert ok is not None
    assert ok["username"] == "carol"

    bad_pw = await auth_service.login(LoginRequest(username="carol", password="wrong"))
    assert bad_pw is None

    missing = await auth_service.login(LoginRequest(username="nobody", password="secret123"))
    assert missing is None


@pytest.mark.asyncio
async def test_signup_returns_uuid_user_id(auth_service):
    user = await auth_service.signup(SignUpRequest(username="dave", password="secret123"))
    assert isinstance(user["user_id"], str)
    assert len(user["user_id"]) == 36
