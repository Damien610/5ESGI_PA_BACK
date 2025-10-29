import pytest
import os
from unittest.mock import patch, MagicMock
from app.models.client import Client

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock des variables d'environnement pour les tests"""
    env_vars = {
        'POSTGRES_USER': 'test',
        'POSTGRES_PASSWORD': 'test',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'SMTP_SERVER': 'smtp.test.com',
        'SMTP_PORT': '587',
        'SMTP_USER': 'test@test.com',
        'SMTP_PASSWORD': 'testpass'
    }
    with patch.dict(os.environ, env_vars):
        yield

@pytest.fixture
def mock_db():
    """Mock de la session de base de données"""
    return MagicMock()

@pytest.fixture
def sample_client():
    """Client d'exemple pour les tests"""
    return Client(
        id_client=1,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        uuid="test-uuid-123",
        loyalty_code="LOYAL123",
        active=False
    )