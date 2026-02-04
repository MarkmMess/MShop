from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from .mixins import UserRelationMixin

from .base import Base

if TYPE_CHECKING:
    from .user import User


# class Profile(UserRelationMixin, Base):
class Profile(Base):
    _user_id_unique = True

    first_name: Mapped[str | None] = mapped_column(String[40])
    last_name: Mapped[str | None] = mapped_column(String[40])
    bio: Mapped[str | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="profile")

    def __str__(self):
        return f"{self.__class__.__name__}(first_name:{self.first_name!r}, last_name:{self.last_name!r})"

    def __repr__(self):
        return str(self)
