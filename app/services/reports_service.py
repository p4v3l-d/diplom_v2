from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.payment import Payment
from ..models.contract import Contract


class ReportsService:
    
    @staticmethod
    def get_payments_by_date_range(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Payment]:
        """
        Возвращает платежи за указанный период.
        """
        query = db.query(Payment)
        
        if start_date:
            query = query.filter(Payment.payment_date >= start_date)
        if end_date:
            query = query.filter(Payment.payment_date <= end_date)

        return query.all()

    @staticmethod
    def get_payments_summary_by_date_range(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """
        Возвращает сводную сумму платежей за период.
        """
        query = db.query(func.sum(Payment.amount))
        
        if start_date:
            query = query.filter(Payment.payment_date >= start_date)
        if end_date:
            query = query.filter(Payment.payment_date <= end_date)
            
        total = query.scalar() or 0
        return {"total_payments_sum": total}

    @staticmethod
    def get_debtors_list(db: Session) -> List[dict]:
        """
        Возвращает список должников (у кого remaining_amount > 0).
        """
        contracts = db.query(Contract).all()
        debtors = []
        
        for contract in contracts:
            if contract.remaining_amount > 0:
                student = contract.student
                debtors.append({
                    "student_id": student.id,
                    "full_name": student.full_name,
                    "contract_id": contract.id,
                    "debt": contract.remaining_amount
                })
        
        return debtors

    @staticmethod
    def get_overall_summary(db: Session) -> dict:
        """
        Возвращает общую сводку:
        - количество платежей
        - сумма оплаченных платежей (status="paid")
        - количество должников
        """
        # Общее количество платежей
        total_payments = db.query(Payment).count()
        
        # Сумма оплаченных платежей
        paid_sum = db.query(func.sum(Payment.amount)).filter(
            Payment.status == "paid"
        ).scalar() or 0
        
        # Количество должников
        all_contracts = db.query(Contract).all()
        debtor_count = sum(1 for c in all_contracts if c.remaining_amount > 0)

        return {
            "total_payments": total_payments,
            "total_paid_sum": paid_sum,
            "debtor_count": debtor_count
        }

    @staticmethod
    def get_payments_statistics(db: Session) -> dict:
        """
        Дополнительная статистика по платежам.
        """
        # Статусы платежей
        statuses = db.query(
            Payment.status, 
            func.count(Payment.id).label('count'),
            func.sum(Payment.amount).label('sum')
        ).group_by(Payment.status).all()
        
        stats = {}
        for status, count, amount_sum in statuses:
            stats[status] = {
                "count": count,
                "total_amount": amount_sum or 0
            }
        
        return {
            "payment_statistics": stats,
            "total_payments_count": db.query(Payment).count(),
            "total_amount": db.query(func.sum(Payment.amount)).scalar() or 0
        }