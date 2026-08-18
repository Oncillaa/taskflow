import datetime
from datetime import UTC

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.v1.endpoints.notifications import create_notification
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate

router = APIRouter(prefix="/tasks", tags=["Задачи"])

@router.post("")
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        deadline=task.deadline,
        assigned_to=task.assigned_to,
        created_by=current_user.id,
        created_at=datetime.datetime.now(UTC)
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    create_notification(message=f"Задача {new_task.title} создана.", user_id=current_user.id)
    return new_task

@router.get("")
async def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    tasks = db.query(Task).filter(Task.created_by == user_id).all()
    return tasks

@router.get("/{id}")
async def get_task_by_id(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    return task

@router.put("/{id}")
async def get_task_by_id(update_task: TaskCreate, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # 3️⃣ Проверяем, что это задача текущего пользователя (опционально)
    if task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование")
    task.assigned_to = update_task.assigned_to
    task.deadline = update_task.deadline
    task.description = update_task.description
    task.priority = update_task.priority
    task.status = update_task.status
    task.title = update_task.title
    db.commit()
    db.refresh(task)
    create_notification(message=f"Задача {task.title} обновлена.", user_id=current_user.id)
    return task

@router.delete("/{id}")
async def get_task_by_id(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

        # 3️⃣ Проверяем, что это задача текущего пользователя
    if task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
    db.delete(task)
    db.commit()
    create_notification(message=f"Задача {task.title} удалена.", user_id=current_user.id)
    # 5️⃣ Возвращаем ответ
    return {"message": f"Задача {id} удалена"}