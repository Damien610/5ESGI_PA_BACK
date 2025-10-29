import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from app.repositories.client_repository import ClientRepository
from app.models.client import Client
from app.exceptions import NotFoundError

@pytest.fixture
def client_repository(mock_db):
    """Fixture pour créer un repository client avec une DB mockée"""
    return ClientRepository(mock_db)

def test_create_client(client_repository, sample_client):
    """Test de création de client"""
    client_repository.db.add = MagicMock()
    client_repository.db.commit = MagicMock()
    client_repository.db.refresh = MagicMock()
    
    result = client_repository.create(sample_client)
    
    assert result == sample_client
    client_repository.db.add.assert_called_once_with(sample_client)
    client_repository.db.commit.assert_called_once()
    client_repository.db.refresh.assert_called_once_with(sample_client)

def test_get_by_email_success(client_repository, sample_client):
    """Test de récupération de client par email - succès"""
    mock_query = MagicMock()
    client_repository.db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = sample_client
    
    result = client_repository.get_by_email("test@example.com")
    
    assert result == sample_client

def test_get_by_email_not_found(client_repository):
    """Test de récupération de client par email - non trouvé"""
    mock_query = MagicMock()
    client_repository.db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    
    with pytest.raises(NotFoundError, match="Costumer not found"):
        client_repository.get_by_email("notfound@example.com")

def test_update_otp(client_repository, sample_client):
    """Test de mise à jour OTP"""
    otp_hash = "abc123"
    expiration = datetime.utcnow() + timedelta(minutes=10)
    
    client_repository.db.commit = MagicMock()
    client_repository.db.refresh = MagicMock()
    
    result = client_repository.update_otp(sample_client, otp_hash, expiration)
    
    assert result.otp_hash == otp_hash
    assert result.otp_hash_expiration == expiration
    client_repository.db.commit.assert_called_once()
    client_repository.db.refresh.assert_called_once_with(sample_client)

def test_activate_client(client_repository, sample_client):
    """Test d'activation de client"""
    client_repository.db.commit = MagicMock()
    
    result = client_repository.activate_client(sample_client)
    
    assert result.active is True
    assert result.otp_hash is None
    assert result.otp_hash_expiration is None
    client_repository.db.commit.assert_called_once()