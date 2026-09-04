# this library is used to define the relationship between the table A and table B in the database
# In this case, the relationship is between the User table and the Collection table
from __future__ import annotations

# this library is used for treate the IDE checker know there are existing classes in the other files, so it can be used in this file
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.db import Base

if TYPE_CHECKING:
    from src.api.database.models.collections import Collection


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    collections: Mapped[list["Collection"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
