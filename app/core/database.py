from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Путь к базе данных внутри контейнера
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "taskflow.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()