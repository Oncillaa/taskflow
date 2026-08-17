from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.endpoints.users import get_current_user
from app.core.database import get_db
from app.models.notifications import Notification
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Уведомления"])

@router.get("")
async def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).all()
    return notifications
@router.patch("/{id}/read")
async def read_notification(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), id: int | None = None):
    my_notification = db.query(Notification).filter(Notification.id == id).first()
    my_notification.is_read = True
    db.commit()
    return {"detail": "Уведомление помечено как прочитанное."}
