import datetime
from datetime import UTC


import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def hash_password(password: str):
    password_encode = password.encode("utf-8")
    password_hash = bcrypt.hashpw(password_encode, bcrypt.gensalt())
    return password_hash.decode("utf-8")

def check_password(password: str, password_hash: str):
    password_encode = password.encode("utf-8")
    password_hash_encode = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_encode, password_hash_encode)

def create_access_token(username: str):
    payload = {
        "sub": username,
        "exp": (datetime.datetime.now(UTC) + datetime.timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]  # ✅ должно быть списком!
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен просрочен")
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload:
        try:
            user = db.query(User).filter(User.username == payload["sub"]).first()
            return user
        except:
            raise HTTPException(status_code=401, detail="Непредвиденная ошибка")
    else:
        raise HTTPException(status_code=401, detail="Ошибка авторизации")