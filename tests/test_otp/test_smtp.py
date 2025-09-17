import os
from dotenv import load_dotenv
from app.utils.otp_service import send_otp_email

load_dotenv()

# Test d'envoi
email_test = "damien.nerri@gmail.com"
otp_test = "123456"

if send_otp_email(email_test, otp_test):
    print("✅ Email envoyé avec succès")
else:
    print("❌ Erreur d'envoi")