from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserOut, TokenResponse
from ..auth.deps import get_current_user, require_role
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, 
             db: Session = Depends(get_db), 
             current_user=Depends(require_role(["ADMIN"]))):
    """
    Регистрирует нового пользователя. Для этого требуется быть ADMIN.
    """
    return auth_service.register_user(db, user_in)

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для логина, ожидает form-data (username, password).
    Возвращает JWT-токен при успехе.
    """
    return auth_service.login(db, form_data.username, form_data.password)

@router.get("/whoami", response_model=UserOut)
def whoami(current_user: User = Depends(get_current_user)):
    """
    Тестовый эндпоинт: возвращает данные текущего авторизованного пользователя.
    """
    return current_user