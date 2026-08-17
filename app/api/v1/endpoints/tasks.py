from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status or "pending",
        priority=task_data.priority or "medium",
        deadline=task_data.deadline,
        assigned_to=task_data.assigned_to,
        created_by=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
<<<<<<< HEAD
    new_notification = Notification(
        message=f"Задача {new_task.id} создана",
        is_read=False,
        created_at=datetime.now(UTC),
        user_id=current_user.id,
        username=current_user.username
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
=======

    # 📢 Уведомление, если задача назначена
    if task_data.assigned_to:
        create_notification(
            user_id=task_data.assigned_to,
            message=f"📌 Вам назначена задача: {task_data.title}",
            db=db
        )

>>>>>>> 6d905bf (Сохраняю локальные изменения перед pull)
    return new_task

@router.get("/", response_model=TaskListResponse)
def list_tasks(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    return TaskListResponse(tasks=tasks, total=total)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.created_by != current_user.id and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    task.updated_at = datetime.now()
    db.commit()
    new_notification = Notification(
        message=f"Задача {task_id} обновлена",
        is_read=False,
        created_at=datetime.now(UTC),
        user_id=current_user.id,
        username=current_user.username
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can delete task")
    db.delete(task)
    db.commit()
    return None

@router.patch("/{task_id}/status", response_model=TaskResponse)
def change_task_status(
    task_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    valid_statuses = ["pending", "in_progress", "review", "completed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {valid_statuses}"
        )

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.status
    task.status = new_status
    task.updated_at = datetime.now()
    db.commit()
    db.refresh(task)

    # 📢 Уведомление, если у задачи есть исполнитель
    if task.assigned_to:
        create_notification(
            user_id=task.assigned_to,
            message=f"🔄 Статус задачи '{task.title}' изменён: {old_status} → {new_status}",
            db=db
        )

    return task

@router.get("/my/", response_model=TaskListResponse)
def get_my_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.assigned_to == current_user.id).all()
    return TaskListResponse(tasks=tasks, total=len(tasks))

@router.get("/created/", response_model=TaskListResponse)
def get_created_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.created_by == current_user.id).all()
    return TaskListResponse(tasks=tasks, total=len(tasks))

@router.get("/{task_id}/graph")
def get_task_graph(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Возвращает граф связей задачи (nodes + edges) для визуализации"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Получаем все задачи пользователя (для узлов)
    user_tasks = db.query(Task).filter(
        (Task.created_by == current_user.id) | (Task.assigned_to == current_user.id)
    ).all()
    
    # Получаем все связи, где участвует данная задача
    links = db.query(Link).filter(
        (Link.task_from == task_id) | (Link.task_to == task_id)
    ).all()
    
    # Строим граф
    nodes = []
    for t in user_tasks:
        nodes.append({
            "id": t.id,
            "label": t.title[:20] + ("..." if len(t.title) > 20 else ""),
            "title": t.title,
            "status": t.status
        })
    
    edges = []
    for link in links:
        edges.append({
            "from": link.task_from,
            "to": link.task_to,
            "label": link.link_type
        })
    
    return {"nodes": nodes, "edges": edges}