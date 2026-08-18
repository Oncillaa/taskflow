from datetime import UTC, datetime


from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.notification import Notification

router = APIRouter(prefix="/notifications")

def create_notification(message: str, user_id: int):
    new_notification = Notification(
        message=message,
        is_read=False,
        user_id=user_id,
        created_at=datetime.now(UTC)
    )
    with SessionLocal() as db:
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
    return True
@router.get("")
async def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).all()
    if notifications:
        return notifications
    return []

@router.patch("/{id}/read")
async def read_notification(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдена")
    if current_user.id != notification.user_id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
    notification.is_read = True
    db.commit()
    return {"detail": "Помечено как прочитанное"}