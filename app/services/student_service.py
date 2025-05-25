from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.student import Student
from ..schemas.student import StudentCreate, StudentUpdate


class StudentService:
    
    @staticmethod
    def search_students(
        db: Session,
        full_name: Optional[str] = None,
        group: Optional[str] = None,
        specialty: Optional[str] = None
    ) -> List[Student]:
        """
        Поиск студентов по ФИО, группе и/или специальности.
        """
        query = db.query(Student)

        if full_name:
            query = query.filter(Student.full_name.ilike(f"%{full_name}%"))
        if group:
            query = query.filter(Student.group.ilike(f"%{group}%"))
        if specialty:
            query = query.filter(Student.specialty.ilike(f"%{specialty}%"))

        return query.all()

    @staticmethod
    def get_all_students(db: Session) -> List[Student]:
        """
        Возвращает список всех студентов.
        """
        return db.query(Student).all()

    @staticmethod
    def create_student(db: Session, student_in: StudentCreate) -> Student:
        """
        Создаёт запись о новом студенте.
        """
        new_student = Student(**student_in.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

    @staticmethod
    def get_student_by_id(db: Session, student_id: int) -> Student:
        """
        Возвращает данные о студенте по ID.
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    @staticmethod
    def check_student_access(current_user, student_id: int) -> bool:
        """
        Проверяет, может ли пользователь получить доступ к данным студента.
        """
        if current_user.role == "STUDENT" and current_user.student_id != student_id:
            return False
        return True

    @staticmethod
    def update_student(db: Session, student_id: int, student_in: StudentUpdate) -> Student:
        """
        Обновляет информацию о студенте.
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        for field, value in student_in.dict(exclude_unset=True).items():
            setattr(student, field, value)

        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def delete_student(db: Session, student_id: int) -> dict:
        """
        Удаляет студента из БД.
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        db.delete(student)
        db.commit()
        return {"detail": "Student deleted"}