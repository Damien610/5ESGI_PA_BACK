import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
import time

from .core.config import settings
from .db import init_db
from .exceptions import BaseAPIException
from .error_handler import (
    api_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from .middleware.security import SecurityHeadersMiddleware, RateLimitMiddleware

from app.api.routers import storage_router, client_router, terminal_router, restaurant_router

# Configuration du logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Borne Appétit API")
    logger.info("✅ Database connection successful")
    try:
        from app.services.storage_service import storage_service
        storage_service.ensure_bucket_exists()
        logger.info("✅ Storage service initialized")
    except Exception as e:
        logger.error(f"❌ Storage service initialization failed: {e}")
    yield
    logger.info("👋 Shutdown complete")

app = FastAPI(
    title="Borne Appétit API",
    description="API d'authentification OTP pour système de fidélité client",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.debug
)

# Security middleware
app.add_middleware(SecurityHeadersMiddleware)
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*.borneappetit.com", "localhost"]
    )
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)
else:
    app.add_middleware(RateLimitMiddleware, calls=10, period=60)  # 10 req/min pour tests

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS middleware with secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    return response

# Enregistrement des gestionnaires d'erreurs
app.add_exception_handler(BaseAPIException, api_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Routes
app.include_router(storage_router.router, prefix="/api/v1")
app.include_router(client_router.router, prefix="/api/v1")
app.include_router(terminal_router.router, prefix="/api/v1")
app.include_router(restaurant_router.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "Borne Appétit API is running",
        "version": "1.0.0",
        "environment": settings.environment
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "timestamp": time.time()
    }
