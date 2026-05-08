from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base

class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=True)