from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.models.task import Task
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkResponse

router = APIRouter(prefix="/links", tags=["links"])

@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def create_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверяем, что обе задачи существуют
    task_from = db.query(Task).filter(Task.id == link_data.task_from).first()
    task_to = db.query(Task).filter(Task.id == link_data.task_to).first()
    if not task_from or not task_to:
        raise HTTPException(status_code=404, detail="One or both tasks not found")
    
    # Проверяем, что пользователь имеет доступ хотя бы к одной из задач
    if task_from.created_by != current_user.id and task_from.assigned_to != current_user.id:
        if task_to.created_by != current_user.id and task_to.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    new_link = Link(
        task_from=link_data.task_from,
        task_to=link_data.task_to,
        link_type=link_data.link_type or "related_to"
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    link_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    task = db.query(Task).filter(Task.id == link.task_from).first()
    if task and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(link)
    db.commit()
    return None

@router.get("/task/{task_id}", response_model=List[LinkResponse])
def get_task_links(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    links = db.query(Link).filter(
        (Link.task_from == task_id) | (Link.task_to == task_id)
    ).all()
    return links