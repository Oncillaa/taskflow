import datetime
from datetime import UTC

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, check_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Регистрация", "Вход"])

@router.post("/register")
async def user_register(user: UserCreate, db: Session = Depends(get_db)):
    existing_username = db.query(User).filter(User.username == user.username).first()
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    elif existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        password_hash = hash_password(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=password_hash,
            is_active=False,
            created_at=datetime.datetime.now(UTC)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"detail": "Успешная регистрация!"}

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    check_username = db.query(User).filter(User.username == user.username).first()
    if check_username:
        password_hash = check_username.hashed_password
        if check_password(user.password, password_hash):
            token = create_access_token(user.username)
            return {
                "access_token": token
            }
        else:
            raise HTTPException(status_code=401, detail="Пароль неверный")
    else:
        raise HTTPException(status_code=401, detail="Такого пользователя не существует")