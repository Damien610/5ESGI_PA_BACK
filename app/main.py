from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from .db import init_db
from .exceptions import BaseAPIException
from .error_handler import (
    api_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler,
    general_exception_handler
)

from app.routes import calcul, client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Database connection successful")
    yield
    print("👋 Shutdown complete")

app = FastAPI(lifespan=lifespan)

# Enregistrement des gestionnaires d'erreurs
app.add_exception_handler(BaseAPIException, api_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(calcul.router)
app.include_router(client.router)

async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Borne appétit API is running"}
