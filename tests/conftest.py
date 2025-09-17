import pytest
import os
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock des variables d'environnement pour les tests"""
    env_vars = {
        'POSTGRES_USER': 'test',
        'POSTGRES_PASSWORD': 'test',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db'
    }
    with patch.dict(os.environ, env_vars):
        yield