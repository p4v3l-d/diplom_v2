from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.contract import Contract
from ..schemas.contract import ContractCreate


class ContractService:
    
    @staticmethod
    def create_contract(db: Session, contract_in: ContractCreate) -> Contract:
        """
        Создаёт новый договор.
        """
        new_contract = Contract(**contract_in.dict())
        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)
        return new_contract

    @staticmethod
    def get_all_contracts(db: Session) -> List[Contract]:
        """
        Возвращает все договоры.
        """
        return db.query(Contract).all()

    @staticmethod
    def get_contract_by_id(db: Session, contract_id: int) -> Contract:
        """
        Возвращает договор по ID.
        """
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return contract

    @staticmethod
    def update_contract(db: Session, contract_id: int, contract_in: ContractCreate) -> Contract:
        """
        Обновляет договор.
        """
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        for field, value in contract_in.dict(exclude_unset=True).items():
            setattr(contract, field, value)

        db.commit()
        db.refresh(contract)
        return contract

    @staticmethod
    def delete_contract(db: Session, contract_id: int) -> dict:
        """
        Удаляет договор.
        """
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        db.delete(contract)
        db.commit()
        return {"detail": "Contract deleted"}

    @staticmethod
    def get_contracts_with_debt(db: Session) -> List[dict]:
        """
        Возвращает список договоров с задолженностью.
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