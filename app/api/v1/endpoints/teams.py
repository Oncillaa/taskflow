from datetime import UTC, datetime

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.v1.endpoints.notifications import create_notification
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.team import Team
from app.models.user import User
from app.schemas.team import TeamCreate

router = APIRouter(prefix="/teams")

@router.post("")
async def create_team(team: TeamCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_team = Team(
        name=team.name,
        description=team.description,
        created_by=current_user.id,
        members=[current_user.id],
        created_at=datetime.now(UTC)
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    create_notification(message=f"Команда {new_team.name} создана.", user_id=current_user.id)
    return {"detail": "Команда успешно создана."}

@router.get("")
async def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teams = db.query(Team).filter().all()
    current_teams = [i for i in teams if current_user.id in i.members]
    return current_teams