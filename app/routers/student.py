from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..schemas.student import StudentCreate, StudentUpdate, StudentInDB
from ..auth.deps import get_current_user, require_role
from ..services.student_service import StudentService


router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/search", response_model=List[StudentInDB])
def search_students(
    full_name: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Эндпоинт для поиска студентов по ФИО, группе и/или специальности.
    Все параметры необязательны, если какой-то параметр не передан — фильтр по нему не применяется.
    """
    return StudentService.search_students(db, full_name, group, specialty)

@router.get("/", response_model=List[StudentInDB])
def get_students(db: Session = Depends(get_db), 
                 current_user: User = Depends(get_current_user)):
    """
    Возвращает список всех студентов.
    Доступно любому авторизованному пользователю.
    """
    return StudentService.get_all_students(db)

@router.post("/", response_model=StudentInDB)
def create_student(student_in: StudentCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    """
    Создаёт запись о новом студенте. 
    Требует роль ADMIN или ACCOUNTANT.
    """
    return StudentService.create_student(db, student_in)

@router.get("/{student_id}", response_model=StudentInDB)
def get_student_by_id(student_id: int, 
                      db: Session = Depends(get_db), 
                      current_user: User = Depends(get_current_user)):
    """
    Возвращает данные о студенте по ID.
    Доступно любому авторизованному пользователю, но 
    студент может смотреть только о себе (если у него есть привязка).
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    # Проверяем права доступа
    if not StudentService.check_student_access(current_user, student_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return student

@router.put("/{student_id}", response_model=StudentInDB)
def update_student(student_id: int,
                   student_in: StudentUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    """
    Обновляет информацию о студенте.
    Требует роль ADMIN или ACCOUNTANT.
    """
    return StudentService.update_student(db, student_id, student_in)

@router.delete("/{student_id}")
def delete_student(student_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(require_role(["ADMIN"]))):
    """
    Удаляет студента из БД (предполагается, что без каскадных договоров).
    Требует роль ADMIN.
    """
    return StudentService.delete_student(db, student_id)