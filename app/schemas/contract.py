from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class ContractBase(BaseModel):
    contract_number: str
    date_signed: date
    valid_until: Optional[date]
    total_amount: float
    discount: Optional[float] = 0.0
    payment_schedule: str

class ContractCreate(ContractBase):
    student_id: int

class ContractInDB(ContractBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True

class ContractWithPayments(ContractInDB):
    payments: List["PaymentInDBShort"] = []
