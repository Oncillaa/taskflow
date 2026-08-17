from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True