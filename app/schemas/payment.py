from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма > 0")
    payment_date: date
    payment_method: Optional[str] = None
    status: Optional[str] = "unpaid"

class PaymentCreate(PaymentBase):
    contract_id: int

class PaymentUpdate(PaymentBase):
    amount: Optional[float] = None
    payment_date: Optional[date] = None
    status: Optional[str] = None

class PaymentInDB(PaymentBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True
