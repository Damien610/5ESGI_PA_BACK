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

    def get_by_uuid(self, uuid: str) -> Restaurant:
        restaurant = self.db.query(Restaurant).filter(Restaurant.uuid == uuid).first()
        if not restaurant:
            raise NotFoundError("Restaurant not found")
    def get_by_uri(self, uri_name: str) -> Restaurant:
        restaurant = self.db.query(Restaurant).filter(Restaurant.uri_name == uri_name).first()
        if not restaurant:
            raise NotFoundError("Restaurant found")
        return restaurant