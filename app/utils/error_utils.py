from functools import wraps
from sqlalchemy.orm import Session
from app.exceptions import DatabaseError

def handle_db_errors(func):
    """Décorateur pour gérer automatiquement les erreurs de base de données"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = None
        # Trouver la session dans les arguments
        for arg in args:
            if isinstance(arg, Session):
                db_session = arg
                break
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if db_session:
                db_session.rollback()
            # Re-lever les exceptions personnalisées
            if hasattr(e, 'status_code'):
                raise
            # Convertir les autres erreurs en DatabaseError
            raise DatabaseError(f"Erreur base de données: {str(e)}")
    
    return wrapper