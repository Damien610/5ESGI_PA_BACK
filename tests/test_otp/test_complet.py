import requests

print("=== Test complet API OTP ===")

# Test 1: Envoyer OTP
print("1. Envoi OTP...")
response = requests.post("http://localhost:8000/clients/send-otp", 
                        json={"email": "damien.nerri@gmail.com"})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    print("\n✅ OTP envoyé ! Vérifiez votre email.")
    
    # Demander le code OTP
    otp_code = input("\nEntrez le code OTP reçu par email: ")
    
    # Test 2: Vérifier OTP
    print("2. Vérification OTP...")
    response = requests.post("http://localhost:8000/clients/verify-otp", 
                            json={"email": "damien.nerri@gmail.com", "otp_code": otp_code})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ OTP vérifié avec succès !")
    else:
        print("\n❌ Erreur de vérification OTP")
else:
    print("\n❌ Erreur d'envoi OTP")