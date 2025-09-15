from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db import init_db

from app.routes import calcul

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Database connection successful")
    yield
    print("👋 Shutdown complete")

app = FastAPI(lifespan=lifespan)
app.include_router(calcul.router)

async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "API Template Ready"}
