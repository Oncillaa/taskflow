
from sqlalchemy import Integer, Column, String, Boolean, DateTime

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    is_read = Column(Boolean)
    created_at = Column(DateTime)
    user_id = Column(String)
    username = Column(String)