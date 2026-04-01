from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate
from app.models.transaction import Transaction
from app.services.risk_engine import calculate_risk
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transaction")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    risk = calculate_risk(transaction)

    db_txn = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        location=transaction.location,
        device_id=transaction.device_id,
        risk_score=risk,
    )

    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)

    return {"status": "success", "risk_score": risk}
