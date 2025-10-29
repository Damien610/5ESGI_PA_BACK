import random
import hashlib
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sqlalchemy.orm import Session
from app.repositories.client_repository import ClientRepository
from app.exceptions import ValidationError

class OTPService:
    def __init__(self, db: Session):
        self.db = db
        self.client_repo = ClientRepository(db)

    def generate_otp(self) -> str:
        return str(random.randint(100000, 999999))

    def hash_otp(self, otp: str) -> str:
        return hashlib.sha256(otp.encode()).hexdigest()

    def get_expiration(self) -> datetime:
        return datetime.utcnow() + timedelta(minutes=10)

    def send_otp(self, email: str) -> bool:
        client = self.client_repo.get_by_email(email)
        otp = self.generate_otp()
        otp_hash = self.hash_otp(otp)
        expiration = self.get_expiration()
        
        self.client_repo.update_otp(client, otp_hash, expiration)
        return self._send_email(email, otp)

    def verify_otp(self, email: str, otp: str):
        client = self.client_repo.get_by_email(email)
        
        if not client.otp_hash or not client.otp_hash_expiration:
            raise ValidationError("No OTP found for this client")
        
        if datetime.utcnow() > client.otp_hash_expiration:
            raise ValidationError("OTP expired")
        
        if client.otp_hash != self.hash_otp(otp):
            raise ValidationError("OTP invalid")
        
        activated_client = self.client_repo.activate_client(client)
        return activated_client

    def _send_email(self, email: str, otp: str) -> bool:
        try:
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_user = os.getenv("SMTP_USER", "borneappetit0@gmail.com")
            smtp_password = os.getenv("SMTP_PASSWORD", "garr egub sndo qpxl")
            
            if not smtp_user or not smtp_password:
                return False
            
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = "Code de vérification"
            
            body = f"Votre code de vérification est : {otp}\n\nCe code expire dans 5 minutes."
            msg.attach(MIMEText(body, 'plain'))
            
            if smtp_port == 465:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False