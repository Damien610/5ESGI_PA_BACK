import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "borneappetit0@gmail.com")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "garr egub sndo qpxl")
    otp_expiration_minutes: int = 5

settings = Settings()