from datetime import datetime, timezone

# from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


from .base import Base
from .user import User


#
# if TYPE_CHECKING:
#     from .order import Order
#     from .order_product_association import OrderProductAssociation
#


# class Product(UserRelationMixin, Base):
class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    username: Mapped[str] = mapped_column(
        ForeignKey("users.username", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(back_populates="products")
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products",
    # )

    # orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
    #     back_populates="product",
    # )
