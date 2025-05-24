from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# В реальном проекте строку подключения (DATABASE_URL) берём из config.py или переменных окружения.
DATABASE_URL = "sqlite:///./app_db.sqlite3"

# Создаём движок:
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # параметр для SQLite
)

# Создаём фабрику сессий:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для наших моделей:
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
