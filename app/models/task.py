from sqlalchemy import Column, Integer, String, DateTime

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    deadline = Column(String, nullable=True)
    assigned_to = Column(String, nullable=True)
    created_by = Column(Integer)
    created_at = Column(DateTime)