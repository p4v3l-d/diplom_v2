# # my_app/routers/payment.py

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from ..database import get_db
# from ..models.payment import Payment
# from ..schemas.payment import PaymentCreate, PaymentInDB
# from ..auth.deps import get_current_user, require_role
# from ..models.user import User

# router = APIRouter(prefix="/payments", tags=["Платежи"])

# @router.post("/", response_model=PaymentInDB)
# def create_payment(payment_in: PaymentCreate,
#                    db: Session = Depends(get_db),
#                    current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
#     new_payment = Payment(**payment_in.dict())
#     db.add(new_payment)
#     db.commit()
#     db.refresh(new_payment)
#     return new_payment

# @router.get("/", response_model=List[PaymentInDB])
# def get_all_payments(db: Session = Depends(get_db),
#                      current_user: User = Depends(get_current_user)):
#     return db.query(Payment).all()

# @router.get("/{payment_id}", response_model=PaymentInDB)
# def get_payment(payment_id: int,
#                 db: Session = Depends(get_db),
#                 current_user: User = Depends(get_current_user)):
#     payment = db.query(Payment).filter(Payment.id == payment_id).first()
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")
#     return payment

# @router.delete("/{payment_id}")
# def delete_payment(payment_id: int,
#                    db: Session = Depends(get_db),
#                    current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
#     payment = db.query(Payment).filter(Payment.id == payment_id).first()
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")

#     db.delete(payment)
#     db.commit()
#     return {"detail": "Payment deleted"}

# @router.get("/{payment_id}/receipt")
# def generate_receipt(payment_id: int, db: Session = Depends(get_db),
#                      current_user: User = Depends(get_current_user)):
#     """
#     Генерирует "квитанцию" по платёжке.
#     Упрощённый пример: возвращаем просто текст. 
#     В реальном проекте можно генерировать PDF.
#     """
#     payment = db.query(Payment).filter(Payment.id == payment_id).first()
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")

#     # Вытаскиваем данные о студенте через связь contract -> student
#     contract = payment.contract
#     student = contract.student  # если настроено relationship

#     receipt_content = (
#         f"Квитанция об оплате №{payment.id}\n"
#         f"Студент: {student.full_name}\n"
#         f"Сумма: {payment.amount}\n"
#         f"Дата: {payment.payment_date}\n"
#         f"Статус: {payment.status}\n"
#     )
#     # В реальной практике вернём PDF/HTML, тут - упрощённо текст
#     return {"receipt": receipt_content}

# @router.patch("/{payment_id}/status")
# def update_payment_status(
#     payment_id: int,
#     new_status: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))
# ):
#     """
#     Меняет статус платежа (например, 'unpaid' -> 'paid').
#     new_status может быть: 'paid', 'canceled', etc.
#     """
#     payment = db.query(Payment).filter(Payment.id == payment_id).first()
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")

#     payment.status = new_status
#     db.commit()
#     db.refresh(payment)
#     return {"detail": f"Payment status updated to {new_status}"}

# routers/payment.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import get_db
from ..models.payment import Payment
from ..models.contract import Contract
from ..schemas.payment import PaymentCreate, PaymentInDB, PaymentUpdate
from ..auth.deps import get_current_user, require_role
from ..models.user import User

router = APIRouter(prefix="/payments", tags=["Платежи"])

@router.post("/", response_model=PaymentInDB)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN","ACCOUNTANT"]))
):
    contract = db.query(Contract).filter(Contract.id == payment_in.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")

    new_payment = Payment(
        contract_id=payment_in.contract_id,
        amount=payment_in.amount,
        payment_date=payment_in.payment_date,
        payment_method=payment_in.payment_method,
        status=payment_in.status or "unpaid"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=List[PaymentInDB])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payments = db.query(Payment).all()
    return payments

@router.patch("/{payment_id}", response_model=PaymentInDB)
def update_payment_status(
    payment_id: int,
    payment_upd: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN","ACCOUNTANT"]))
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Платёж не найден")

    # Обновим только те поля, которые пришли
    update_data = payment_upd.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)

    db.commit()
    db.refresh(payment)
    return payment

@router.get("/{payment_id}/receipt")
def generate_receipt(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Упрощенная квитанция (текст).
    Реально можно генерировать PDF/HTML с реквизитами.
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Платёж не найден")

    contract = payment.contract
    # student = contract.student  # если нужно вывести данные студента
    receipt_text = (
        f"Квитанция №{payment.id}\n"
        f"Контракт №{contract.contract_number}\n"
        f"Сумма: {payment.amount} руб.\n"
        f"Дата платежа: {payment.payment_date}\n"
        f"Статус: {payment.status}\n"
        f"Способ: {payment.payment_method}\n"
        f"Остаток по контракту: {contract.remaining_amount}\n"
        "Спасибо за оплату!"
    )
    return {"receipt": receipt_text}
