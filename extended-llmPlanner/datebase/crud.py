from datebase.db import engine, base, sessionLocal, Tasks
from datetime import datetime

def add_task(name, dateinsert, datefinish, status):
    session = sessionLocal()
    
    task = Tasks(
        name=name, 
        dateinsert=datetime.now(),
        datefinish=datetime.now(),
        status=status
    )
    session.add(task)
    session.commit()
    return task.id