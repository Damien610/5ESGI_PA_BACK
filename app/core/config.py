import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "borneappetit0@gmail.com")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "garr egub sndo qpxl")
    otp_expiration_minutes: int = 5
    
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "minio-dev:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "uploads")

settings = Settings()