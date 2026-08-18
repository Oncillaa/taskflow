from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Имя пользователя (3-50 символов)"
    )
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Пароль (минимум 8 символов)"
    )
class UserLogin(BaseModel):
    username: str
    password: str

