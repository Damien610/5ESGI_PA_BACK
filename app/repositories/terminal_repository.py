from sqlalchemy.orm import Session
from app.exceptions import NotFoundError
from app.models.terminal import Terminal

class TerminalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_uuid(self, uuid: str) -> Terminal:
        terminal = self.db.query(Terminal).filter(Terminal.uuid == uuid).first()
        if not terminal:
            raise NotFoundError("Terminal not found")
        return terminal