import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(url=os.getenv('POSTGRE_PATH'))

sessio_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

def get_db() -> Session:
    db = sessio_factory()
    try:
        yield db
    finally:
        db.close()