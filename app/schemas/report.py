from pydantic import BaseModel
from datetime import date

class PaymentReportItem(BaseModel):
    payment_id: int
    amount: float
    payment_date: date
    status: str

    class Config:
        from_attributes = True
