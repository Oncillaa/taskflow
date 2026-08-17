from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.v1.endpoints.users import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["Команды"])
@router.post("")
async def create_team_func(current_user: User = Depends(get_current_user)):
    pass

@router.get("")
async def get_teams_func():
    pass