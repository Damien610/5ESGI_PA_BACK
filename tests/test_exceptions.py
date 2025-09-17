import pytest
from app.exceptions import (
    BaseAPIException, 
    NotFoundError, 
    AlreadyExistError, 
    ValidationError, 
    DatabaseError, 
    BusinessLogicError
)

def test_base_api_exception():
    """Test de l'exception de base"""
    exc = BaseAPIException("Test message", 500)
    assert exc.message == "Test message"
    assert exc.status_code == 500

def test_not_found_error():
    """Test de l'erreur 404"""
    exc = NotFoundError("Resource not found")
    assert exc.message == "Resource not found"
    assert exc.status_code == 404

def test_already_exist_error():
    """Test de l'erreur 409"""
    exc = AlreadyExistError("Already exists")
    assert exc.message == "Already exists"
    assert exc.status_code == 409

def test_validation_error():
    """Test de l'erreur 400"""
    exc = ValidationError("Invalid data")
    assert exc.message == "Invalid data"
    assert exc.status_code == 400

def test_database_error():
    """Test de l'erreur 500"""
    exc = DatabaseError("DB error")
    assert exc.message == "DB error"
    assert exc.status_code == 500

def test_business_logic_error():
    """Test de l'erreur 422"""
    exc = BusinessLogicError("Logic error")
    assert exc.message == "Logic error"
    assert exc.status_code == 422