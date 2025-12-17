from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.restaurant.restaurant import RestaurantRead
from app.schemas.style.style import StyleRead
from app.schemas.terminal.schemas_terminal import RegistrationResponse
from app.schemas.terminal.terminal import TerminalRead
from app.services.terminal_service import TerminalService

router = APIRouter(prefix="/terminal", tags=["terminal"])

@router.get("/config/{uuid}", response_model=RegistrationResponse)
def get_config_by_uuid(uuid: str, db: Session = Depends(get_db)):
    terminal_service = TerminalService(db)
    terminal, restaurant, styles = terminal_service.get_config_by_uuid(uuid)
    return {
        "terminal": TerminalRead.model_validate(terminal),
        "restaurant": RestaurantRead.model_validate(restaurant),
        "styles": [StyleRead.model_validate(s) for s in styles],
    }