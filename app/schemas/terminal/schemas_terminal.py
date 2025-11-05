from pydantic import BaseModel

from app.schemas.restaurant.restaurant import RestaurantRead
from app.schemas.style.style import StyleRead
from app.schemas.terminal.terminal import TerminalRead

class RegistrationResponse(BaseModel):
    terminal: TerminalRead
    restaurant: RestaurantRead
    styles: list[StyleRead]

    class Config:
        from_attributes = True