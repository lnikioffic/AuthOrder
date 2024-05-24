from datetime import datetime   
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.order.models import Order
from src.product.models import DataSet


class User(Base):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    is_active: Mapped[bool] = mapped_column(server_default='false', default=True)
    is_superuser: Mapped[bool] = mapped_column(server_default='false', default=False)
    is_verified: Mapped[bool] = mapped_column(server_default='false', default=False)

    orders_user: Mapped[list['Order']] = relationship(
        back_populates='user'
    )

    datasets: Mapped[list['DataSet']] = relationship(
        back_populates='user'
    )