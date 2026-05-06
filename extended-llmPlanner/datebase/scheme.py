from sqlalchemy import (create_engine, 
    Column, Integer, String, DateTime)
from datebase.db import Base

class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dateinsert = Column(DateTime)
    datefinish = Column(DateTime)
    status = Column(String(50))