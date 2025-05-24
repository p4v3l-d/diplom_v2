from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from ..database import get_db
from ..models.user import User
from .jwt_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
"""
tokenUrl="/auth/login" означает, что в Swagger UI будет поле для username/password,
и запрос пойдёт именно на эндпоинт POST /auth/login
"""

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Извлекает user по токену. 
    Если токен недействителен/просрочен/несоответствует - выбрасывается 401.
    """
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token payload",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token or expired token",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found",
        )
    return user

def require_role(allowed_roles: list[str]):
    """
    Фабрика зависимостей: позволяет указать список ролей,
    которые имеют доступ к эндпоинту. 
    Пример: current_user = Depends(require_role(["ADMIN", "ACCOUNTANT"]))
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not enough permissions",
            )
        return current_user
    return role_checker
