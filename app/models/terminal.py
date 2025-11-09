from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

class Terminal(Base):
    __tablename__ = "terminal"

    id_terminal = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)

    id_restaurant = Column(Integer, ForeignKey('restaurant.id_restaurant'), nullable=False)
    restaurant = relationship("Restaurant", back_populates="terminals")
