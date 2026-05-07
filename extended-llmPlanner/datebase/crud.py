from datebase.db import sessio_factory
from datebase.scheme import Tasks
from datetime import datetime
from typing import List

class DBaseQuery:
    @staticmethod
    def create_task(task: Tasks) -> Tasks:
        """ Создает новую таску """
        with sessio_factory() as session:
            new_task = Tasks(
                name=task.name, 
                dateinsert=task.datetime.now(),
                datefinish=task.datetime.now(),
                status=task.status
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return new_task
        
    @staticmethod
    def read_task() -> List[Tasks]:
        """ Возвращает все таски """
        with sessio_factory() as session:
            tasks = session.query(Tasks).all() 
            return [
                {
                    "id": task.id,
                    "name": task.name,
                    "status": task.status
                }
                for task in tasks
            ]

    @staticmethod
    def read_task_id(task_id: id):
        """ Возвращает таску по id """
        with sessio_factory() as session:
            task = session.query(Tasks).filter(Tasks.id == task_id).first
            return task

    @staticmethod
    def update_task(task_id: int, new_name: str):
        """ Обновляет таску по id """
        with sessio_factory() as session:
            task = session.query(Tasks).filter(Tasks.id == task_id).first()
            if not task:
                return None
            task.name = new_name
            session.commit()
            session.refresh(task)
            return task

    @staticmethod
    def delete_task():
        pass