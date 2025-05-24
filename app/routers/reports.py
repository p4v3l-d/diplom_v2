# routers/reports.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..auth.deps import get_current_user, require_role
from ..models.payment import Payment
from ..models.contract import Contract
from ..schemas.payment import PaymentInDB

router = APIRouter(prefix="/reports", tags=["Отчёты"])

@router.get("/payments-range", response_model=List[PaymentInDB])
def payments_range(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Отчёт о платежах за указанный период [start_date, end_date].
    Если даты не указаны, выбираем все платежи.
    """
    query = db.query(Payment)
    if start_date:
        query = query.filter(Payment.payment_date >= start_date)
    if end_date:
        query = query.filter(Payment.payment_date <= end_date)

    return query.all()

@router.get("/payments-range/summary")
def payments_range_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Сводная сумма по платежам за период.
    """
    query = db.query(func.sum(Payment.amount))
    if start_date:
        query = query.filter(Payment.payment_date >= start_date)
    if end_date:
        query = query.filter(Payment.payment_date <= end_date)
    total = query.scalar() or 0
    return {"total_payments_sum": total}

@router.get("/debtors")
def get_debtors(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["ADMIN","ACCOUNTANT"]))
):
    """
    Список должников: у кого remaining_amount > 0
    """
    contracts = db.query(Contract).all()
    debtors = []
    for c in contracts:
        if c.remaining_amount > 0:
            st = c.student
            debtors.append({
                "student_id": st.id,
                "full_name": st.full_name,
                "contract_id": c.id,
                "debt": c.remaining_amount
            })
    return debtors

@router.get("/summary")
def get_overall_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Пример общей сводки:
    - кол-во платежей
    - сумма оплаченных (status="paid")
    - кол-во должников
    """
    total_payments = db.query(Payment).count()
    paid_sum = db.query(func.sum(Payment.amount)).filter(Payment.status=="paid").scalar() or 0
    # должники:
    all_contracts = db.query(Contract).all()
    debtor_count = sum(1 for c in all_contracts if c.remaining_amount > 0)

    return {
        "total_payments": total_payments,
        "total_paid_sum": paid_sum,
        "debtor_count": debtor_count
    }
