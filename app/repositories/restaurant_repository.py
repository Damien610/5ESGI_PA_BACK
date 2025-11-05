from sqlalchemy.orm import Session
from app.exceptions import NotFoundError
from app.models import Restaurant

class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Restaurant:
        restaurant = self.db.query(Restaurant).filter(Restaurant.id_restaurant == id).first()
        if not restaurant:
            raise NotFoundError("Restaurant found")
        return restaurant