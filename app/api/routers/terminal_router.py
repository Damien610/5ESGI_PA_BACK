from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.client.client_response import ClientResponse
from app.services.terminal_service import TerminalService

router = APIRouter(prefix="/terminal", tags=["terminal"])

@router.get("/register/{uuid}")
def register_terminal(uuid: str, db: Session = Depends(get_db)):
    terminal_service = TerminalService(db)
    terminal = terminal_service.register_terminal(uuid)
    return terminal