from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.client.schemas_client import OTPRequest, OTPVerify, OTPResponse
from app.schemas.client.client_create import ClientCreate
from app.schemas.client.client_response import ClientResponse
from app.dependencies import get_db
from app.services.otp_service import OTPService
from app.services.client_service import ClientService
from app.exceptions import ValidationError

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/create")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    client_service = ClientService(db)
    client_service.create_client(
        first_name=client.first_name,
        last_name=client.last_name,
        email=client.email,
        restaurant_uuid=client.restaurant_uuid,
        uuid=client.uuid,
        loyalty_code=client.loyalty_code
    )
    return {"message": "Client créé et OTP envoyé", "email": client.email}

@router.post("/send-otp", response_model=OTPResponse)
def send_otp(request: OTPRequest, db: Session = Depends(get_db)):
    otp_service = OTPService(db)
    
    if not otp_service.send_otp(request.email):
        raise ValidationError("Erreur lors de l'envoi de l'email")
    
    return OTPResponse(message="Code OTP envoyé par email", success=True)

@router.post("/verify-otp", response_model=ClientResponse)
def verify_otp(request: OTPVerify, db: Session = Depends(get_db)):
    otp_service = OTPService(db)
    activated_client = otp_service.verify_otp(request.email, request.otp_code)
    return activated_client

@router.get("/{email}", response_model=ClientResponse)
def get_client(email: str, db: Session = Depends(get_db)):
    client_service = ClientService(db)
    client = client_service.get_client_by_email(email)
    return client

