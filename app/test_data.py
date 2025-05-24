# app/seeds.py
from datetime import date, timedelta

from .models.student import Student
from .models.contract import Contract
from .models.payment import Payment
from .database import SessionLocal


def seed_test_data() -> None:
    """Заполняет базу примером, если она ещё пуста."""
    with SessionLocal() as db:
        # уже запускали? – выходим
        if db.query(Student).first():
            return

        # ======== 1. Студент =========
        student = Student(
            full_name="Иванов Иван Иванович",
            birth_date=date(2000, 1, 1),
            passport_number="1234 567890",
            group="ИСП-19-1",
            specialty="Программирование",
            contacts="+7 800 555-35-35",
        )
        db.add(student)
        db.flush()                      # получаем student.id

        # ======== 2. Договор =========
        contract = Contract(
            contract_number="Договор-0001",
            student_id=student.id,
            date_signed=date(2025, 5, 1),
            valid_until=date(2026, 5, 1),
            total_amount=100_000,
            discount=0,
            payment_schedule="помесячно",
        )
        db.add(contract)
        db.flush()

        # ======== 3. Платежи 01–20 мая 2025 г. =========
        pay_day = date(2025, 5, 1)
        while pay_day <= date(2025, 5, 20):
            db.add(
                Payment(
                    contract_id=contract.id,
                    amount=5_000,                # примерная сумма
                    payment_date=pay_day,
                    payment_method="наличные",
                    status="unpaid",
                )
            )
            pay_day += timedelta(days=10)

        db.commit()
