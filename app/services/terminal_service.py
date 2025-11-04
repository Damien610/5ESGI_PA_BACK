from sqlalchemy.orm import Session
from app.models.terminal import Terminal
from app.repositories.style_repository import StyleRepository
from app.repositories.terminal_repository import TerminalRepository

class TerminalService:
    def __init__(self, db: Session):
        self.db = db
        self.terminal_repo = TerminalRepository(db)
        self.style_repo = StyleRepository(db)

    def register_terminal(self, uuid: str) -> Terminal:
        terminal = self.terminal_repo.get_by_uuid(uuid)
        styles = self.style_repo.get_by_restaurant_id(terminal.id_restaurant)

        return styles