from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.deps import get_current_user, require_role
from ..schemas.payment import PaymentInDB
from ..services.reports_service import ReportsService

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
    return ReportsService.get_payments_by_date_range(db, start_date, end_date)

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
    return ReportsService.get_payments_summary_by_date_range(db, start_date, end_date)

@router.get("/debtors")
def get_debtors(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["ADMIN","ACCOUNTANT"]))
):
    """
    Список должников: у кого remaining_amount > 0
    """
    return ReportsService.get_debtors_list(db)

@router.get("/summary")
def get_overall_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Общая сводка:
    - кол-во платежей
    - сумма оплаченных (status="paid")
    - кол-во должников
    """
    return ReportsService.get_overall_summary(db)

@router.get("/statistics")
def get_payments_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Дополнительная статистика по платежам.
    """
    return ReportsService.get_payments_statistics(db)