from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.models.team import Team, team_members
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse, TeamListResponse

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_team = Team(
        name=team_data.name,
        description=team_data.description,
        created_by=current_user.id
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.get("/", response_model=TeamListResponse)
def list_teams(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    teams = db.query(Team).offset(skip).limit(limit).all()
    total = db.query(Team).count()
    return TeamListResponse(teams=teams, total=total)

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can update team")
    for key, value in team_data.dict(exclude_unset=True).items():
        setattr(team, key, value)
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can delete team")
    db.delete(team)
    db.commit()
    return None

@router.post("/{team_id}/members/{user_id}")
def add_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can add members")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user in team.members:
        raise HTTPException(status_code=400, detail="User already in team")
    team.members.append(user)
    db.commit()
    return {"message": f"User {user_id} added to team {team_id}"}

@router.delete("/{team_id}/members/{user_id}")
def remove_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can remove members")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user not in team.members:
        raise HTTPException(status_code=400, detail="User not in team")
    team.members.remove(user)
    db.commit()
    return {"message": f"User {user_id} removed from team {team_id}"}

@router.get("/{team_id}/members", response_model=List[dict])
def get_team_members(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return [{"id": u.id, "username": u.username, "email": u.email} for u in team.members]