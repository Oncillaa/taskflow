
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    is_read = Column(Boolean)
    user_id = Column(Integer)
    created_at = Column(DateTime)