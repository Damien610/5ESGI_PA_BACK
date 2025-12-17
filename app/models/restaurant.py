from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base

class Restaurant(Base):
    __tablename__ = "restaurant"

    id_restaurant = Column(Integer, primary_key=True, autoincrement=True)
    uri_name = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    logo = Column(String(200), nullable=False)
    favicon = Column(String(200), nullable=False)
    uuid = Column(String(100), nullable=False)

    styles = relationship("Style", back_populates="restaurant", cascade="all, delete-orphan")
    terminals = relationship("Terminal", back_populates="restaurant", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="restaurant", cascade="all, delete-orphan")