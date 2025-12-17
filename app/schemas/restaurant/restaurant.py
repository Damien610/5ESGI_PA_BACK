from pydantic import BaseModel

class RestaurantRead(BaseModel):
    uri_name: str
    name: str
    logo: str
    favicon: str
    uuid: str
    class Config:
        from_attributes = True
