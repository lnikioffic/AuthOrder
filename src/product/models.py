from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from src.models import Base

if TYPE_CHECKING:
    from src.order.models import ProductOrder
    from src.users.models import User


class DataSet(Base):

    __tablename__ = 'dataset'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    type_dataset_id: Mapped[int] = mapped_column(ForeignKey('type_dataset.id'))
    
    price: Mapped[int] = mapped_column(nullable=True)
    
    count_frames: Mapped[int]
    count_classes: Mapped[int]
    
    file_path: Mapped[str] = mapped_column(String(100))
    first_frame: Mapped[str] = mapped_column(String(100))
    second_frame: Mapped[str] = mapped_column(String(100))
    size: Mapped[str]
    
    type_dataset: Mapped['TypeDataset'] = relationship(back_populates='dataset')
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='RESTRICT'))

    user: Mapped['User'] = relationship(
        back_populates='datasets'
    )
    
    # orders: Mapped[list['Order']] = relationship (
    #     secondary='dataset_order',
    #     back_populates='dataset'
    # )
    
    # связь через ассоциативную модель
    orders_details: Mapped[list['ProductOrder']] = relationship(
        back_populates='product'
    )
     
     
class TypeDataset(Base):
    __tablename__ = 'type_dataset'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    dataset: Mapped[list['DataSet']] = relationship(back_populates='type_dataset')