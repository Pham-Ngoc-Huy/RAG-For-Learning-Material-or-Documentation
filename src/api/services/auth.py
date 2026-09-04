from abc import ABC, abstractmethod
from uuid import uuid4

import bcrypt

from src.api.database.db import database, engine, metadata
from src.api.database.models import User


class AuthService(ABC):
    def __init__(self):
        metadata.create_all(engine)
        self.db = database
        self.users = User.__table__

    @abstractmethod
    async def signup(self, requests):
        pass

    @abstractmethod
    async def login(self, requests):
        pass


class AuthServiceImpl(AuthService):
    @staticmethod
    def _hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def _verify_password(password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed)

    async def signup(self, requests):
        query = self.users.select().where(self.users.c.username == requests.username)
        existing_user = await self.db.fetch_one(query)
        if existing_user:
            raise ValueError("Username already exists")
        user_id = str(uuid4())
        hashed_password = self._hash_password(requests.password)
        query = self.users.insert().values(
            user_id=user_id,
            username=requests.username,
            password=hashed_password,
        )
        await self.db.execute(query)
        query = self.users.select().where(self.users.c.user_id == user_id)
        return await self.db.fetch_one(query)

    async def login(self, requests):
        query = self.users.select().where(self.users.c.username == requests.username)
        existing_user = await self.db.fetch_one(query)
        if not existing_user:
            return None
        if not self._verify_password(requests.password, existing_user["password"]):
            return None
        return existing_user
