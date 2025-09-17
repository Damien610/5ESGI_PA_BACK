import os
import sys
sys.path.append('../..')

from dotenv import load_dotenv
load_dotenv('../../.env.dev')

from app.utils.otp_service import send_otp_email, generate_otp

# Test simple
print("Test de generation OTP...")
otp = generate_otp()
print(f"OTP genere: {otp}")

print("\nTest d'envoi email...")
email_test = "damien.nerri@gmail.com"  # Votre email pour recevoir le test

if send_otp_email(email_test, otp):
    print("Email envoye avec succes!")
    print(f"Verifiez votre boite mail: {email_test}")
else:
    print("Erreur d'envoi email")