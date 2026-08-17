from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(CommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True