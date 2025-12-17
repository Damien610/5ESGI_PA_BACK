from sqlalchemy.orm import Session
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.style_repository import StyleRepository
from app.repositories.terminal_repository import TerminalRepository

class TerminalService:
    def __init__(self, db: Session):
        self.db = db
        self.terminal_repo = TerminalRepository(db)
        self.restaurant_repo = RestaurantRepository(db)
        self.style_repo = StyleRepository(db)

    def get_config_by_uuid(self, uuid: str):
        terminal = self.terminal_repo.get_by_uuid(uuid)
        restaurant = self.restaurant_repo.get_by_id(terminal.id_restaurant)
        styles = self.style_repo.get_by_restaurant_id(terminal.id_restaurant)

        return terminal, restaurant, styles