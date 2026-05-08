from database.db import session_factory, Base, engine
from agent.serialize import Task
from database.scheme import Tasks

import json

class DBaseQuery:
    @staticmethod
    def create_tables():
        """ Создает все таблицы """
        Base.metadata.create_all(engine)

    @staticmethod
    def create_task(task: Task) -> str:
        """ Создает новую таску """
        with session_factory() as session:
            new_task = Tasks(
                name=task.name, 
                date=task.date,
                status=task.status
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return json.dumps({
                "id": new_task.id,
                "name": new_task.name,
                "status": new_task.status
            }, ensure_ascii=False)
        
    @staticmethod
    def read_task() -> str:
        """ Возвращает все таски """
        with session_factory() as session:
            tasks = session.query(Tasks).all() 
            return json.dumps([
                {
                    "id": task.id,
                    "name": task.name,
                    "status": task.status
                }
                for task in tasks
            ], ensure_ascii=False)

    @staticmethod
    def read_task_id(task_id: int) -> str:
        """ Возвращает таску по id """
        with session_factory() as session:
            task = session.query(Tasks).filter(Tasks.id == task_id).first()
            return json.dumps({
                "id": task.id,
                "name": task.name,
                "status": task.status
            }, ensure_ascii=False)

    @staticmethod
    def update_task(task_id: int, new_name: str) -> str:
        """ Обновляет таску по id """
        with session_factory() as session:
            task = session.query(Tasks).filter(Tasks.id == task_id).first()
            if not task: return None
            task.name = new_name
            session.commit()
            session.refresh(task)
            return json.dumps({
                "id": task.id,
                "name": task.name,
                "status": task.status
            }, ensure_ascii=False)

    @staticmethod
    def delete_task(task_id: int) -> str:
        """ Удаляет задачу по id """
        with session_factory() as session:
            task = session.query(Tasks).filter(Tasks.id == task_id).first()
            if not task: return None
            session.delete(task)
            session.commit()
            return json.dumps({
                "id": task.id,
                "name": task.name,
                "status": task.status
            }, ensure_ascii=False)