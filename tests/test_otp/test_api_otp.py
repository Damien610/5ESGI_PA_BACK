import requests
import json

# URL de base de votre API
BASE_URL = "http://localhost:8000"

def test_send_otp():
    """Test d'envoi d'OTP"""
    url = f"{BASE_URL}/clients/send-otp"
    data = {
        "email": "damien.nerri@gmail.com"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_verify_otp():
    """Test de vérification d'OTP"""
    otp_code = input("Entrez le code OTP recu par email: ")
    
    url = f"{BASE_URL}/clients/verify-otp"
    data = {
        "email": "damien.nerri@gmail.com",
        "otp_code": otp_code
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    print("=== Test API OTP ===")
    print("1. Test envoi OTP...")
    
    if test_send_otp():
        print("2. Test verification OTP...")
        test_verify_otp()
    else:
        print("Erreur lors de l'envoi OTP")