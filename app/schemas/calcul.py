import pydantic


class CalculCreate(pydantic.BaseModel):
    operande_1: float
    operande_2: float
    operation: str = pydantic.Field(..., min_length=1, max_length=1)


class CalculOut(pydantic.BaseModel):
    operande_1: float
    operande_2: float
    operation: str
    resultat: float

    model_config = pydantic.ConfigDict(from_attributes=True)
