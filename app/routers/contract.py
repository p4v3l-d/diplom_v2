from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.contract import ContractCreate, ContractInDB
from ..auth.deps import get_current_user, require_role
from ..models.user import User
from ..services.contract_service import ContractService

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post("/", response_model=ContractInDB)
def create_contract(contract_in: ContractCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    return ContractService.create_contract(db, contract_in)

@router.get("/", response_model=List[ContractInDB])
def get_all_contracts(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return ContractService.get_all_contracts(db)

@router.get("/{contract_id}", response_model=ContractInDB)
def get_contract_by_id(contract_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    return ContractService.get_contract_by_id(db, contract_id)

@router.put("/{contract_id}", response_model=ContractInDB)
def update_contract(contract_id: int,
                    contract_in: ContractCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    return ContractService.update_contract(db, contract_id, contract_in)

@router.delete("/{contract_id}")
def delete_contract(contract_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(require_role(["ADMIN"]))):
    return ContractService.delete_contract(db, contract_id)