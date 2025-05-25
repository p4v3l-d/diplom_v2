import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./app_db.sqlite3"

DATABASE_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/payments"
)

# Создаём движок:
# engine = create_engine(
#     DATABASE_URL, 
#     connect_args={"check_same_thread": False}  # параметр для SQLite
# )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

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
