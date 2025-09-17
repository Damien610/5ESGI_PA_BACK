from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from sqlmodel import Session
from app.exceptions import AlreadyExistError, DatabaseError

def create_customer(database_session: Session, customer_data: CustomerCreate):
    try:
        existing_customer = database_session.query(Customer).filter(Customer.email == customer_data.email).first()

        if existing_customer:
            raise AlreadyExistError("Email déjà enregistré")

        new_customer = Customer(**customer_data.dict(exclude_unset=True))
        database_session.add(new_customer)
        database_session.commit()
        database_session.refresh(new_customer)
        return new_customer
    except Exception as e:
        database_session.rollback()
        if isinstance(e, AlreadyExistError):
            raise
        raise DatabaseError(f"Erreur lors de la création du client: {str(e)}")
