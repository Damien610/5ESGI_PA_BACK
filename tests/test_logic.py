import pytest
from unittest.mock import MagicMock, patch
from app.services.client_service import ClientService
from app.models.client import Client
from app.exceptions import ValidationError

@pytest.fixture
def client_service():
    """Fixture pour créer un service client avec une DB mockée"""
    mock_db = MagicMock()
    return ClientService(mock_db)

@patch('app.services.client_service.OTPService')
def test_create_client_success(mock_otp_service, client_service):
    """Test de création de client réussie"""
    from app.models.restaurant import Restaurant
    
    # Mock du restaurant
    mock_restaurant = Restaurant(
        id_restaurant=1,
        uri_name="test",
        name="Test",
        logo="logo.png",
        uuid="restaurant-uuid"
    )
    client_service.restaurant_repo.get_by_uuid = MagicMock(return_value=mock_restaurant)
    
    # Mock du repository
    client_service.client_repo.create = MagicMock()
    mock_client = Client(
        first_name="Test",
        last_name="User", 
        email="test@example.com",
        uuid="test-uuid",
        loyalty_code="TEST123",
        id_restaurant=1
    )
    client_service.client_repo.create.return_value = mock_client
    
    # Mock du service OTP
    mock_otp_instance = MagicMock()
    mock_otp_service.return_value = mock_otp_instance
    mock_otp_instance.send_otp.return_value = True
    client_service.otp_service = mock_otp_instance
    
    result = client_service.create_client("Test", "User", "test@example.com", "restaurant-uuid", "test-uuid", "TEST123")
    
    assert result == mock_client
    client_service.client_repo.create.assert_called_once()
    mock_otp_instance.send_otp.assert_called_once_with("test@example.com")

@patch('app.services.client_service.OTPService')
def test_create_client_otp_failure(mock_otp_service, client_service):
    """Test de création de client avec échec d'envoi OTP"""
    from app.models.restaurant import Restaurant
    
    # Mock du restaurant
    mock_restaurant = Restaurant(
        id_restaurant=1,
        uri_name="test",
        name="Test",
        logo="logo.png",
        uuid="restaurant-uuid"
    )
    client_service.restaurant_repo.get_by_uuid = MagicMock(return_value=mock_restaurant)
    client_service.client_repo.create = MagicMock()
    
    # Mock du service OTP qui échoue
    mock_otp_instance = MagicMock()
    mock_otp_service.return_value = mock_otp_instance
    mock_otp_instance.send_otp.return_value = False
    client_service.otp_service = mock_otp_instance
    
    with pytest.raises(ValidationError, match="Erreur lors de l'envoi de l'email de vérification"):
        client_service.create_client("Test", "User", "test@example.com", "restaurant-uuid", "test-uuid", "TEST123")

def test_get_client_by_email(client_service):
    """Test de récupération de client par email"""
    mock_client = Client(email="test@example.com")
    client_service.client_repo.get_by_email = MagicMock(return_value=mock_client)
    
    result = client_service.get_client_by_email("test@example.com")
    
    assert result == mock_client
    client_service.client_repo.get_by_email.assert_called_once_with("test@example.com")
