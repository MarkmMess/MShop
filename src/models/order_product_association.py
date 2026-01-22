from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from . import Order, Product
from .base import Base


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="idx_order_product_association",
        ),
    )

    id: Mapped[int] = Column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey(Order.id))
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id))
    count: Mapped[int] = mapped_column(default=1, server_default="1")
