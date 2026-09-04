from pathlib import Path

from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parents[1] / 'users.db'}"


class Base(DeclarativeBase):
    pass


database = Database(DATABASE_URL)
metadata = Base.metadata
engine = create_engine(DATABASE_URL)
