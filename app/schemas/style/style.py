from pydantic import BaseModel

class StyleRead(BaseModel):
    uuid: str
    name: str
    style_value: str

    class Config:
        from_attributes = True