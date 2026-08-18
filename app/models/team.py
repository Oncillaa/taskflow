from sqlalchemy import Column, Integer, String, JSON, DateTime

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_by = Column(Integer)
    members = Column(JSON, default=[])
    created_at = Column(DateTime)