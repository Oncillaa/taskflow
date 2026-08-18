from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users")
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user