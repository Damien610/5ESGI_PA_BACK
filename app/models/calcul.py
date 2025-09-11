from sqlalchemy import Column, Integer, Float, String
from app.db import Base

class Calcul(Base):
    __tablename__ = "calculs"

    id = Column(Integer, primary_key=True, index=True)
    operande_1 = Column(Float, nullable=False)
    operande_2 = Column(Float, nullable=False)
    operation = Column(String(1), nullable=False)
    resultat = Column(Float, nullable=False)
