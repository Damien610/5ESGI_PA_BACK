import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.services.otp_service import OTPService

@pytest.fixture
def otp_service():
    """Fixture pour créer un service OTP avec une DB mockée"""
    mock_db = MagicMock()
    return OTPService(mock_db)

def test_generate_otp(otp_service):
    """Test de génération d'OTP"""
    otp = otp_service.generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()

def test_hash_otp(otp_service):
    """Test de hashage d'OTP"""
    otp = "123456"
    hashed = otp_service.hash_otp(otp)
    assert len(hashed) == 64  # SHA-256 = 64 caractères
    assert hashed != otp

def test_get_expiration(otp_service):
    """Test de calcul d'expiration"""
    expiration = otp_service.get_expiration()
    now = datetime.utcnow()
    assert expiration > now
    assert expiration <= now + timedelta(minutes=11)

@patch('app.services.otp_service.smtplib.SMTP')
@patch('app.services.otp_service.os.getenv')
def test_send_email_success(mock_getenv, mock_smtp, otp_service):
    """Test d'envoi d'email réussi"""
    mock_getenv.side_effect = lambda key, default=None: {
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': '587',
        'SMTP_USER': 'test@gmail.com',
        'SMTP_PASSWORD': 'password'
    }.get(key, default)
    
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server
    
    result = otp_service._send_email("test@gmail.com", "123456")
    
    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()

@patch('app.services.otp_service.os.getenv')
def test_send_email_missing_config(mock_getenv, otp_service):
    """Test d'envoi d'email avec configuration manquante"""
    mock_getenv.return_value = ""
    
    result = otp_service._send_email("test@gmail.com", "123456")
    
    assert result is False