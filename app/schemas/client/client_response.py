from pydantic import BaseModel

class ClientResponse(BaseModel):
    id_client: int
    first_name: str
    last_name: str
    email: str
    active: bool
    
    class Config:
        from_attributes = True