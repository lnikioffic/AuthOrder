from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.product.models import Product

if TYPE_CHECKING:
    from src.users.models import User


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int | None]
    payment: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(
        back_populates='orders_user'
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    products: Mapped[list['Product']] = relationship(
        secondary='product_order',
        back_populates='orders'
    )


class ProductOrder(Base):
    __tablename__ = 'product_order'
    __table_args__ = (UniqueConstraint('order_id', 'product_id', name='idx_unique'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))