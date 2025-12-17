from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.restaurant.restaurant import RestaurantRead
from app.schemas.style.style import StyleRead
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurant", tags=["Restaurant"])

@router.get("/{uri}/config")
def get_restaurant_by_uri(uri: str, db: Session = Depends(get_db)):
    restaurant_service = RestaurantService(db)
    restaurant, styles = restaurant_service.get_restaurant_config_by_uri(uri)
    return {
        "restaurant": RestaurantRead.model_validate(restaurant),
        "styles": [StyleRead.model_validate(s) for s in styles],
    }