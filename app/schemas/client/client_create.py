from uuid import uuid4
from pydantic import BaseModel, Field, root_validator
import random
import string


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    restaurant_uuid: str
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    loyalty_code: str | None = None

    #génération automatique du code de fidélité avant la validation des données
    @root_validator(pre=True)
    def generate_loyalty_code(cls, values):
        first = values.get("first_name", "").strip().upper()
        last = values.get("last_name", "").strip().upper()

        random_digits = ''.join(random.choices(string.digits, k=4))

        code = f"{last[:4]}{first[:3]}-{random_digits}"

        values["loyalty_code"] = code
        return values


