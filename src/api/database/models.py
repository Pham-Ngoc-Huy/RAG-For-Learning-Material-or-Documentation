from database.db import metadata
from sqlalchemy import Column, Integer, String, Table

users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False, index=True),
    Column("password", String, nullable=False),
)


collections = Table(
    "collections",
    metadata,
    Column("collection_id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False, foreign_key="users.user_id"),
    Column("collection_name", String(100), nullable=False),
)
