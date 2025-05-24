from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class StudentBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=200)
    birth_date: Optional[date] = None
    passport_number: Optional[str] = None
    group: Optional[str] = None
    specialty: Optional[str] = None
    course: Optional[int] = None
    contacts: Optional[str] = None

class StudentCreate(StudentBase):
    # поля, необходимые для создания, можно добавить при необходимости
    pass

class StudentUpdate(StudentBase):
    # поля, необходимые для изменения, допускается оставлять те же
    pass

class StudentInDB(StudentBase):
    id: int

    class Config:
        orm_mode = True

class StudentWithContracts(StudentInDB):
    contracts: List = []
