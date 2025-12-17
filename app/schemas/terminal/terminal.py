from pydantic import BaseModel

class TerminalRead(BaseModel):
    name: str
    uuid: str
    class Config:
        from_attributes = True
