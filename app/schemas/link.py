from pydantic import BaseModel
from typing import Optional

class LinkBase(BaseModel):
    task_from: int
    task_to: int
    link_type: Optional[str] = "related_to"

class LinkCreate(LinkBase):
    pass

class LinkResponse(LinkBase):
    id: int

    class Config:
        from_attributes = True