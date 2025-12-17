from sqlalchemy.orm import Session
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.style_repository import StyleRepository

class RestaurantService:
    def __init__(self, db: Session):
        self.db = db
        self.restaurant_repo = RestaurantRepository(db)
        self.style_repo = StyleRepository(db)

    def get_restaurant_config_by_uri(self, uri: str):
        restaurant = self.restaurant_repo.get_by_uri(uri)
        styles = self.style_repo.get_by_restaurant_id(restaurant.id_restaurant)
        return restaurant, styles