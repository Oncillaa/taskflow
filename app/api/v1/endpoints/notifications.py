<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
=======
from datetime import datetime, UTC

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from app.api.v1.endpoints.users import get_current_user
from app.core.database import get_db, SessionLocal
from app.models.notifications import Notification
>>>>>>> 61bb31d (Добавлены ручки команд (не все) и некоторые уведомления)
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()
    return notifications

@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your notification")

    notification.is_read = True
    db.commit()
<<<<<<< HEAD
    return {"message": "Notification marked as read"}
=======
    return {"detail": "Уведомление помечено как прочитанное."}

def create_notification(message: str, current_user: User):
    with SessionLocal() as db:
        new_notification = Notification(
            message=message,
            is_read=False,
            created_at=datetime.now(UTC),
            user_id=current_user.id,
            username=current_user.username
        )
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
>>>>>>> 61bb31d (Добавлены ручки команд (не все) и некоторые уведомления)
