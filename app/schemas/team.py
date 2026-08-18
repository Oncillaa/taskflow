from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    description: str