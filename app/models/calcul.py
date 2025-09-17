import sqlalchemy
from app.db import Base

class Calcul(Base):
    __tablename__ = "calculs"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    operande_1 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    operande_2 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    operation = sqlalchemy.Column(sqlalchemy.String(1), nullable=False)
    resultat = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
