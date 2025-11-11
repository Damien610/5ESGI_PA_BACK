from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from .db import init_db
from .exceptions import BaseAPIException
from .error_handler import (
    api_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler,
    general_exception_handler
)

from app.api.routers import storage_router, client_router, terminal_router, restaurant_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Database connection successful")
    from app.services.storage_service import storage_service
    storage_service.ensure_bucket_exists()
    yield
    print("👋 Shutdown complete")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des gestionnaires d'erreurs
app.add_exception_handler(BaseAPIException, api_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(storage_router.router)
app.include_router(client_router.router)
app.include_router(terminal_router.router)
app.include_router(restaurant_router.router)

async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Borne appétit API is running"}
