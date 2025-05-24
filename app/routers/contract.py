# my_app/routers/contract.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.contract import Contract
from ..schemas.contract import ContractCreate, ContractInDB
from ..auth.deps import get_current_user, require_role
from ..models.user import User

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post("/", response_model=ContractInDB)
def create_contract(contract_in: ContractCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    new_contract = Contract(**contract_in.dict())
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract

@router.get("/", response_model=List[ContractInDB])
def get_all_contracts(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return db.query(Contract).all()

@router.get("/{contract_id}", response_model=ContractInDB)
def get_contract_by_id(contract_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router.put("/{contract_id}", response_model=ContractInDB)
def update_contract(contract_id: int,
                    contract_in: ContractCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    for field, value in contract_in.dict(exclude_unset=True).items():
        setattr(contract, field, value)

    db.commit()
    db.refresh(contract)
    return contract

@router.delete("/{contract_id}")
def delete_contract(contract_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(require_role(["ADMIN"]))):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(contract)
    db.commit()
    return {"detail": "Contract deleted"}
