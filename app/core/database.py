from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from app.config import settings
load_dotenv()
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/db"
engine = create_engine(DATABASE_URL, echo=True) # Создание движка для работы с бд
Base = declarative_base() # Создание класса для таблиц бд
SessionLocal = sessionmaker(bind=engine) # Создание сессии бд

def get_db(): # Функция для импорта сессии
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()