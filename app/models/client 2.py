from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "client"
    
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(100), nullable=True)
    loyalty_code = Column(String(100), nullable=True, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    otp_hash = Column(String(64), nullable=True)
    otp_hash_expiration = Column(DateTime, nullable=True)
    active = Column(Boolean, default=False)