from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import hashlib

from app.config import settings

# Соль для хэширования
SALT = "taskflow_salt_2026"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль с SHA256 хешем"""
    return get_password_hash(plain_password) == hashed_password

def get_password_hash(password: str) -> str:
    """Генерирует SHA256 хеш пароля с солью"""
    return hashlib.sha256((SALT + password).encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None