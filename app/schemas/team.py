from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TeamResponse(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    members: Optional[List[int]] = []  # список ID, а не объектов

    class Config:
        from_attributes = True

class TeamListResponse(BaseModel):
    teams: List[TeamResponse]
    total: int