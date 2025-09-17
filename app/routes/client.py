from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.client import OTPRequest, OTPVerify, OTPResponse
from app.dependencies import get_db
from app.crud.client import update_client_otp, verify_client_otp
from app.utils.otp_service import generate_otp, hash_otp, get_otp_expiration, send_otp_email
from app.exceptions import ValidationError

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/send-otp", response_model=OTPResponse)
def send_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """Génère et envoie un code OTP par email"""
    otp = generate_otp()
    otp_hash = hash_otp(otp)
    expiration = get_otp_expiration()
    
    # Sauvegarder l'OTP en base
    update_client_otp(db, request.email, otp_hash, expiration)
    
    # Envoyer par email
    if not send_otp_email(request.email, otp):
        raise ValidationError("Erreur lors de l'envoi de l'email")
    
    return OTPResponse(message="Code OTP envoyé par email", success=True)

@router.post("/verify-otp", response_model=OTPResponse)
def verify_otp(request: OTPVerify, db: Session = Depends(get_db)):
    """Vérifie un code OTP"""
    verify_client_otp(db, request.email, request.otp_code)
    return OTPResponse(message="Code OTP vérifié avec succès", success=True)