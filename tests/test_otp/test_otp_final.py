import requests
import json

BASE_URL = "http://localhost:8000"

print("=== Test API OTP ===")

# Test 1: Envoyer OTP
print("1. Test envoi OTP...")
response = requests.post(f"{BASE_URL}/clients/send-otp", 
                        json={"email": "damien.nerri@gmail.com"})

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    print("\nVerifiez votre email et entrez le code OTP recu:")
    otp_code = input("Code OTP: ")
    
    # Test 2: Verifier OTP
    print("2. Test verification OTP...")
    response = requests.post(f"{BASE_URL}/clients/verify-otp", 
                            json={"email": "damien.nerri@gmail.com", "otp_code": otp_code})
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
else:
    print("Erreur lors de l'envoi OTP")