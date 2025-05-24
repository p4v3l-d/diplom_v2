from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserOut, TokenResponse
from ..auth.jwt_handler import create_access_token
from ..auth.deps import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db), 
             current_user=Depends(require_role(["ADMIN"]))):
    """
    Регистрирует нового пользователя. Для этого требуется быть ADMIN.
    """
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use"
        )
    hashed_pwd = pwd_context.hash(user_in.password)
    new_user = User(
        username=user_in.username,
        hashed_password=hashed_pwd,
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для логина, ожидает form-data (username, password).
    Возвращает JWT-токен при успехе.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(subject=user.id)
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.get("/whoami", response_model=UserOut)
def whoami(current_user: User = Depends(get_current_user)):
    """
    Тестовый эндпоинт: возвращает данные текущего авторизованного пользователя.
    """
    return current_user
