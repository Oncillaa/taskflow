from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    deadline: str | None = None
    assigned_to: int | None = None