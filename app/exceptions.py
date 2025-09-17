class BaseAPIException(Exception):
    """Exception de base pour l'API"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(BaseAPIException):
    """Erreur 404 - Ressource non trouvée"""
    def __init__(self, message: str = "Ressource non trouvée"):
        super().__init__(message, 404)

class AlreadyExistError(BaseAPIException):
    """Erreur 409 - Ressource déjà existante"""
    def __init__(self, message: str = "Ressource déjà existante"):
        super().__init__(message, 409)

class ValidationError(BaseAPIException):
    """Erreur 400 - Données invalides"""
    def __init__(self, message: str = "Données invalides"):
        super().__init__(message, 400)

class DatabaseError(BaseAPIException):
    """Erreur 500 - Erreur base de données"""
    def __init__(self, message: str = "Erreur base de données"):
        super().__init__(message, 500)

class BusinessLogicError(BaseAPIException):
    """Erreur 422 - Erreur de logique métier"""
    def __init__(self, message: str = "Erreur de logique métier"):
        super().__init__(message, 422)