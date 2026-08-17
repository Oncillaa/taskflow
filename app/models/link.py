from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    task_from = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task_to = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    link_type = Column(String(50), default="related_to")  # depends_on, blocks, related_to, subtask

    # Связи (чтобы можно было получить объекты задач)
    from_task = relationship("Task", foreign_keys=[task_from])
    to_task = relationship("Task", foreign_keys=[task_to])