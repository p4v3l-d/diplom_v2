from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from ..database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    passport_number = Column(String, nullable=True, unique=True)
    group = Column(String, nullable=True)
    specialty = Column(String, nullable=True)
    course = Column(Integer, nullable=True)
    contacts = Column(String, nullable=True)

    contracts = relationship("Contract", back_populates="student")
