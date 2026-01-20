from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .mixins import UserRelationMixin

from .base import Base


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String[40])
    last_name: Mapped[str | None] = mapped_column(String[40])
    bio: Mapped[str | None]

    def __str__(self):
        return f"{self.__class__.__name__}(first_name:{self.first_name!r}, last_name:{self.last_name!r})"

    def __repr__(self):
        return str(self)
