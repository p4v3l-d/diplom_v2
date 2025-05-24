from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..models.user import User
from ..schemas.student import StudentCreate, StudentUpdate, StudentInDB
from ..auth.deps import get_current_user, require_role


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
    query = db.query(Student)

    if full_name:
        query = query.filter(Student.full_name.ilike(f"%{full_name}%"))
    if group:
        query = query.filter(Student.group.ilike(f"%{group}%"))
    if specialty:
        query = query.filter(Student.specialty.ilike(f"%{specialty}%"))

    results = query.all()
    return results

@router.get("/", response_model=List[StudentInDB])
def get_students(db: Session = Depends(get_db), 
                 current_user: User = Depends(get_current_user)):
    """
    Возвращает список всех студентов.
    Доступно любому авторизованному пользователю.
    """
    return db.query(Student).all()

@router.post("/", response_model=StudentInDB)
def create_student(student_in: StudentCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(require_role(["ADMIN", "ACCOUNTANT"]))):
    """
    Создаёт запись о новом студенте. 
    Требует роль ADMIN или ACCOUNTANT.
    """
    new_student = Student(**student_in.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/{student_id}", response_model=StudentInDB)
def get_student_by_id(student_id: int, 
                      db: Session = Depends(get_db), 
                      current_user: User = Depends(get_current_user)):
    """
    Возвращает данные о студенте по ID.
    Доступно любому авторизованному пользователю, но 
    студент может смотреть только о себе (если у него есть привязка).
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Если роль студента, проверяем, что он смотрит свои данные
    if current_user.role == "STUDENT" and current_user.student_id != student_id:
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
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in student_in.dict(exclude_unset=True).items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(require_role(["ADMIN"]))):
    """
    Удаляет студента из БД (предполагается, что без каскадных договоров).
    Требует роль ADMIN.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"detail": "Student deleted"}
