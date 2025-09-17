from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "client"
    
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(32), nullable=False)
    loyalty_code = Column(String(10), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False, unique=True)
    otp_hash = Column(String(64), nullable=True)
    otp_hash_expiration = Column(DateTime, nullable=True)