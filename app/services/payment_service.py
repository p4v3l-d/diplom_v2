from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.payment import Payment
from ..models.contract import Contract
from ..schemas.payment import PaymentCreate, PaymentUpdate

class PaymentService:
    @staticmethod
    def create(db: Session, dto: PaymentCreate) -> Payment:
        contract = db.query(Contract).filter_by(id=dto.contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Контракт не найден")
        payment = Payment(**dto.dict(exclude={"status"}), status=dto.status or "unpaid")
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def list_all(db: Session) -> list[Payment]:
        return db.query(Payment).all()

    @staticmethod
    def update(db: Session, payment_id: int, dto: PaymentUpdate) -> Payment:
        payment = db.query(Payment).filter_by(id=payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Платёж не найден")
        for k, v in dto.dict(exclude_unset=True).items():
            setattr(payment, k, v)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def generate_receipt(payment: Payment) -> str:
        contract = payment.contract
        return (
            f"Квитанция №{payment.id}\n"
            f"Контракт №{contract.contract_number}\n"
            f"Сумма: {payment.amount} руб.\n"
            f"Дата платежа: {payment.payment_date}\n"
            f"Статус: {payment.status}\n"
            f"Способ: {payment.payment_method}\n"
            f"Остаток по контракту: {contract.remaining_amount}\n"
            "Спасибо за оплату!"
        )
