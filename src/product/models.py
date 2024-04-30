from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.order.models import Order


class Product(Base):

    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fromat: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(default=1, server_default='1')

    orders: Mapped[list['Order']] = relationship (
        secondary='product_order',
        back_populates='products'
    )