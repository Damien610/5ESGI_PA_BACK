from sqlalchemy.orm import Session
from datetime import datetime
from app.models.client import Client
from app.exceptions import NotFoundError

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_by_email(self, email: str) -> Client:
        client = self.db.query(Client).filter(Client.email == email).first()
        if not client:
            raise NotFoundError("Costumer not found")
        return client

    def update_otp(self, client: Client, otp_hash: str, expiration: datetime) -> Client:
        client.otp_hash = otp_hash
        client.otp_hash_expiration = expiration
        self.db.commit()
        self.db.refresh(client)
        return client

    def clear_otp(self, client: Client) -> Client:
        client.otp_hash = None
        client.otp_hash_expiration = None
        self.db.commit()
        return client

    def activate_client(self, client: Client) -> Client:
        client.active = True
        client.otp_hash = None
        client.otp_hash_expiration = None
        self.db.commit()
        return client