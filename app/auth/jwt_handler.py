import time
from typing import Optional, Union
from jose import jwt, JWTError

# Константы для токена
SECRET_KEY = "SOME_LONG_RANDOM_SECRET_KEY"   # в реальном проекте - хранить в .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # час

def create_access_token(
    subject: Union[str, int],
    expires_delta: Optional[int] = None
) -> str:
    """
    Создаёт JWT-токен с полем "sub" = subject (ID пользователя).
    expires_delta - время жизни токена в минутах.
    """
    if expires_delta is None:
        expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES

    to_encode = {"sub": str(subject)}
    expire = int(time.time()) + expires_delta * 60
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Проверяет JWT-токен и возвращает пейлоад (dict) или вызывает исключение JWTError.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # внутри должен быть "sub", "exp" и т. д.
    except JWTError:
        raise
