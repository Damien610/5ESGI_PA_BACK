from sqlalchemy.orm import Session
from app.exceptions import NotFoundError
from app.models import Style

class StyleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_restaurant_id(self, id: int) -> Style:
        styles = self.db.query(Style).filter(Style.id_restaurant == id).all()
        if not styles:
            raise NotFoundError("Styles found")
        return styles