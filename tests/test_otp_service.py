import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.utils.otp_service import generate_otp, hash_otp, get_otp_expiration, send_otp_email

def test_generate_otp():
    """Test de génération d'OTP"""
    otp = generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()

def test_hash_otp():
    """Test de hashage d'OTP"""
    otp = "123456"
    hashed = hash_otp(otp)
    assert len(hashed) == 64  # SHA-256 = 64 caractères
    assert hashed != otp

def test_get_otp_expiration():
    """Test de calcul d'expiration"""
    expiration = get_otp_expiration()
    now = datetime.utcnow()
    assert expiration > now
    assert expiration <= now + timedelta(minutes=6)

@patch('app.utils.otp_service.smtplib.SMTP')
@patch('app.utils.otp_service.os.getenv')
def test_send_otp_email_success(mock_getenv, mock_smtp):
    """Test d'envoi d'email réussi"""
    # Mock des variables d'environnement
    mock_getenv.side_effect = lambda key, default=None: {
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': '587',
        'SMTP_USER': 'damien.nerri@gmail',
        'SMTP_PASSWORD': 'dqgc wrax detu kqra'
    }.get(key, default)
    
    # Mock du serveur SMTP
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server
    
    result = send_otp_email("damien.nerri@gmail", "123456")
    
    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()

@patch('app.utils.otp_service.os.getenv')
def test_send_otp_email_missing_config(mock_getenv):
    """Test d'envoi d'email avec configuration manquante"""
    mock_getenv.return_value = ""
    
    result = send_otp_email("damien.nerri@gmail", "123456")
    
    assert result is False