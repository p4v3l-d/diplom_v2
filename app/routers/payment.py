from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.payment import PaymentCreate, PaymentInDB, PaymentUpdate
from ..auth.deps import get_current_user, require_role
from ..models.user import User
from ..models.payment import Payment
from ..services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Платежи"])
svc = PaymentService  # alias для компактности

@router.post("/", response_model=PaymentInDB)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))
):
    return svc.create(db, payment_in)

@router.get("/", response_model=List[PaymentInDB])
def get_all_payments(db: Session = Depends(get_db),
                     _: User = Depends(get_current_user)):
    return svc.list_all(db)

@router.patch("/{payment_id}", response_model=PaymentInDB)
def update_payment(payment_id: int,
                   payment_upd: PaymentUpdate,
                   db: Session = Depends(get_db),
                   _: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    return svc.update(db, payment_id, payment_upd)

@router.get("/{payment_id}/receipt")
def receipt(payment_id: int,
            db: Session = Depends(get_db),
            _: User = Depends(get_current_user)):
    payment = db.query(Payment).filter_by(id=payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Платёж не найден")
    return {"receipt": svc.generate_receipt(payment)}
