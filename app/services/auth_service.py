from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..models.user import User
from ..schemas.user import UserCreate
from ..auth.jwt_handler import create_access_token


class AuthService:
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Регистрирует нового пользователя.
        """
        # Проверяем, не занят ли username
        existing = db.query(User).filter(User.username == user_in.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use"
            )
        
        # Хешируем пароль
        hashed_pwd = self.pwd_context.hash(user_in.password)
        
        # Создаём пользователя
        new_user = User(
            username=user_in.username,
            hashed_password=hashed_pwd,
            role=user_in.role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def authenticate_user(self, db: Session, username: str, password: str) -> User:
        """
        Аутентифицирует пользователя по username и password.
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=401, 
                detail="Incorrect username or password"
            )

        if not self.pwd_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=401, 
                detail="Incorrect username or password"
            )

        return user

    def create_token_for_user(self, user: User) -> dict:
        """
        Создаёт JWT токен для пользователя.
        """
        access_token = create_access_token(subject=user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def login(self, db: Session, username: str, password: str) -> dict:
        """
        Полный процесс логина: аутентификация + создание токена.
        """
        user = self.authenticate_user(db, username, password)
        return self.create_token_for_user(user)