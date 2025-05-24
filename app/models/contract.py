from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String, unique=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date_signed = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    total_amount = Column(Float, nullable=False)
    discount = Column(Float, nullable=True, default=0.0)
    payment_schedule = Column(String, nullable=False, default="помесячно")

    student = relationship("Student", back_populates="contracts")
    payments = relationship("Payment", back_populates="contract", cascade="all, delete-orphan")

    # Динамическое свойство, не хранится в БД:
    @property
    def paid_amount(self) -> float:
        return sum(p.amount for p in self.payments if p.status == "paid")

    @property
    def remaining_amount(self) -> float:
        return self.total_amount - self.paid_amount if self.total_amount else 0
