from datetime import datetime, timezone

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


from .base import Base
from .user import User


if TYPE_CHECKING:
    from .user import User


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="products")
