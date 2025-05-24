import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uvicorn
from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from .routers import student, contract, payment, auth, reports
from .models.user import User
from fastapi.staticfiles import StaticFiles
from .test_data import seed_test_data

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Payment Management System",
        version="1.0.0",
        description="API для автоматизации учёта оплаты обучения"
    )

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        init_admin(db)
        seed_test_data()

    # Подключаем роутеры
    app.include_router(auth.router)
    app.include_router(student.router)
    app.include_router(contract.router)
    app.include_router(payment.router)
    app.include_router(reports.router)

    app.mount("", StaticFiles(directory="app/static", html=True), name="static-root")
    
    return app

def init_admin(db: Session):
    """
    Создаёт пользователя с username="admin", ролью="ADMIN", если такого нет.
    Пароль по умолчанию "admin123"
    """
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        hashed_pwd = pwd_context.hash("admin123")
        new_admin = User(
            username="admin",
            hashed_password=hashed_pwd,
            role="ADMIN"
        )
        db.add(new_admin)
        db.commit()
        print("Создан пользователь ADMIN с логином=admin и паролем=admin123")


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
