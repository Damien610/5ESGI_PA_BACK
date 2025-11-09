from sqlalchemy import Column,Integer,String,Float,Boolean
from app.db import Base

class Restaurant(Base):
    __tablename__ = "restaurant"

    id_restaurant = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    api_key = Column(String(100), nullable=False, unique=True)
    active = Column(Boolean, default=True)