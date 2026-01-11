from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
