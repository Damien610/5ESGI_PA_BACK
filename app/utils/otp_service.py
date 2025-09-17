import random
import hashlib
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def generate_otp() -> str:
    """Génère un code OTP à 6 chiffres"""
    return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    """Hash le code OTP avec SHA-256"""
    return hashlib.sha256(otp.encode()).hexdigest()

def get_otp_expiration() -> datetime:
    """Retourne l'heure d'expiration (5 minutes)"""
    return datetime.utcnow() + timedelta(minutes=5)

def send_otp_email(email: str, otp: str) -> bool:
    """Envoie l'OTP par email"""
    try:
        # Configuration SMTP (à adapter selon votre fournisseur)
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "damien.nerri@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD", "dqgc wrax detu kqra")
        
        if not smtp_user or not smtp_password:
            print("Configuration SMTP manquante")
            return False
        
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = "Code de vérification"
        
        body = f"""
        Votre code de vérification est : {otp}
        
        Ce code expire dans 5 minutes.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Envoi
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
        
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False