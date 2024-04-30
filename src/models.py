from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass
