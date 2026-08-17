

from sqlalchemy import Integer, Column, String, DateTime, JSON

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime)
    members = Column(JSON, default=list)