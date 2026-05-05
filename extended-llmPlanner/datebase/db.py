from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql+psycopg2://' \
    'postgres:320Me330ls@localhost:5432/planner')

base = declarative_base()

class Tasks(base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dateinsert = Column(DateTime)
    datefinish = Column(DateTime)
    status = Column(String(50))

sessionLocal = sessionmaker(bind=engine)