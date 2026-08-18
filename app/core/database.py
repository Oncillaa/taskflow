from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True) # Создание движка для работы с бд
Base = declarative_base() # Создание класса для таблиц бд
SessionLocal = sessionmaker(bind=engine) # Создание сессии бд

def get_db(): # Функция для импорта сессии
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()