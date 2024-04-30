from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class B(Base):
    __tablename__ = "b"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str]