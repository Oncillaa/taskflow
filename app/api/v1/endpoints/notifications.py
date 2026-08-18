from datetime import UTC, datetime

from fastapi import APIRouter
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
    return notifications