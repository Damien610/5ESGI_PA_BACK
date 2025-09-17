from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import BaseAPIException
import logging

logger = logging.getLogger(__name__)

async def api_exception_handler(request: Request, exc: BaseAPIException):
    """Gestionnaire pour les exceptions personnalisées de l'API"""
    logger.error(f"API Exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "type": exc.__class__.__name__}
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Gestionnaire pour les erreurs SQLAlchemy"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Erreur base de données", "type": "DatabaseError"}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Gestionnaire pour les HTTPException de FastAPI"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "HTTPException"}
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Gestionnaire pour toutes les autres exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Erreur interne du serveur", "type": "InternalServerError"}
    )