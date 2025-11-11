from sqlalchemy.orm import Session
from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.otp_service import OTPService
from app.exceptions import ValidationError

class ClientService:
    def __init__(self, db: Session):
        self.db = db
        self.client_repo = ClientRepository(db)
        self.restaurant_repo = RestaurantRepository(db)
        self.otp_service = OTPService(db)

    def create_client(self, first_name: str, last_name: str, email: str, restaurant_uuid: str, uuid: str, loyalty_code: str) -> Client:
        restaurant = self.restaurant_repo.get_by_uuid(restaurant_uuid)
        
        client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            id_restaurant=restaurant.id_restaurant,
            uuid=uuid,
            loyalty_code=loyalty_code,
            active=False
        )
        
        created_client = self.client_repo.create(client)
        
        # Envoyer OTP automatiquement
        if not self.otp_service.send_otp(email):
            raise ValidationError("Erreur lors de l'envoi de l'email de vérification")
        
        return created_client

    def get_client_by_email(self, email: str) -> Client:
        return self.client_repo.get_by_email(email)