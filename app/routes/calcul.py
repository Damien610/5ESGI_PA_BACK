from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.calcul import Calcul
from app.schemas.calcul import CalculCreate, CalculOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/calculs/", response_model=CalculOut)
def create_calcul(data: CalculCreate, db: Session = Depends(get_db)):
    op1 = data.operande_1
    op2 = data.operande_2

    if data.operation == "+":
        resultat = op1 + op2
    elif data.operation == "-":
        resultat = op1 - op2
    elif data.operation == "*":
        resultat = op1 * op2
    elif data.operation == "/":
        if op2 == 0:
            raise HTTPException(status_code=400, detail="Division par zéro")
        resultat = op1 / op2
    else:
        raise HTTPException(status_code=400, detail="Opération invalide")

    calcul = Calcul(
        operande_1=op1,
        operande_2=op2,
        operation=data.operation,
        resultat=resultat
    )

    db.add(calcul)
    db.commit()
    db.refresh(calcul)

    return calcul
