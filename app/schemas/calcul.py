from pydantic import BaseModel, Field, ConfigDict


class CalculCreate(BaseModel):
    operande_1: float
    operande_2: float
    operation: str = Field(..., min_length=1, max_length=1)


class CalculOut(BaseModel):
    operande_1: float
    operande_2: float
    operation: str
    resultat: float

    model_config = ConfigDict(from_attributes=True)
