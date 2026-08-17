from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

# Таблица связи "многие-ко-многим" для участников команды
team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("User", foreign_keys=[created_by])
    members = relationship("User", secondary=team_members, backref="teams")