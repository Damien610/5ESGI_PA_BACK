from sqlalchemy.orm import Session
from datetime import datetime
from app.models.client import Client
from app.exceptions import NotFoundError, ValidationError
from app.utils.otp_service import hash_otp

def get_client_by_email(db: Session, email: str) -> Client:
    """Récupère un client par email"""
    client = db.query(Client).filter(Client.mail == email).first()
    if not client:
        raise NotFoundError("Client non trouvé")
    return client

def update_client_otp(db: Session, email: str, otp_hash: str, expiration: datetime) -> Client:
    """Met à jour l'OTP d'un client"""
    client = get_client_by_email(db, email)
    client.otp_hash = otp_hash
    client.otp_hash_expiration = expiration
    db.commit()
    db.refresh(client)
    return client

def verify_client_otp(db: Session, email: str, otp: str) -> bool:
    """Vérifie l'OTP d'un client"""
    client = get_client_by_email(db, email)
    
    if not client.otp_hash or not client.otp_hash_expiration:
        raise ValidationError("Aucun OTP en cours")
    
    if datetime.utcnow() > client.otp_hash_expiration:
        raise ValidationError("OTP expiré")
    
    if client.otp_hash != hash_otp(otp):
        raise ValidationError("OTP invalide")
    
    # Nettoyer l'OTP après vérification
    client.otp_hash = None
    client.otp_hash_expiration = None
    db.commit()
    
    return True