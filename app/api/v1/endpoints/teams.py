from datetime import datetime, UTC

import zid
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.v1.endpoints.users import get_current_user
from app.core.database import get_db
from app.models.teams import Team
from app.models.user import User
from app.schemas.teams import TeamCreate

router = APIRouter(prefix="/teams", tags=["Команды"])
@router.post("")
async def create_team_func(current_user: User = Depends(get_current_user), new_team: TeamCreate = None, db: Session = Depends(get_db)):
    team = Team(
        id=zid.zid(),
        name=new_team.name,
        description=new_team.description,
        created_by=current_user.username,
        created_at=datetime.now(UTC),
        members=[current_user.username]
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    return {"name": new_team.name}

@router.get("")
async def get_teams_func(current_user: User = Depends(get_current_user), new_team: TeamCreate = None, db: Session = Depends(get_db)):
    all_teams = db.query(Team).all()
    my_teams = [i for i in all_teams if current_user.username in i.members]
    return {"teams": my_teams, "total": len(my_teams)}