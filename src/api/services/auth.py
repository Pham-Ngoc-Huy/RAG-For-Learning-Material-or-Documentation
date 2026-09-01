from database.db import database, engine, metadata
from database.models import users
from passlib.context import CryptContext


class AuthService:
    def __init__(self):
        metadata.create_all(engine)
        self.db = database
        self.users = users
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def signup(self, requests):
        query = self.users.select().where(self.users.c.username == requests.username)
        existing_user = await self.db.fetch_one(query)
        if existing_user:
            raise ValueError("Username already exists")
        hashed_password = self.pwd_context.hash(requests.password)
        query = self.users.insert().values(
            username=requests.username,
            password=hashed_password,
        )
        await self.db.execute(query)

    async def login(self, requests):
        query = self.users.select().where(self.users.c.username == requests.username)
        existing_user = await self.db.fetch_one(query)
        if not existing_user:
            return None
        if not self.pwd_context.verify(requests.password, existing_user["password"]):
            return None
        return existing_user
