import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(url=os.getenv('POSTGRE_PATH'))

session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

def get_db() -> Session:
    db = session_factory()
    try:
        yield db
    finally:
        db.close()