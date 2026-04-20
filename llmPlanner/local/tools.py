from langchain_core.tools import tool
from db import addTask, getTasks
from datetime import datetime

@tool
def addTaskTool(title: str, date: str, deadline: str, 
            priority: str):
    """ Добавить задачу """
    addTask(title, date, deadline, priority)
    return f"Задача '{title}' добавлена (дедлайн: {deadline})"

@tool
def getTasksListTool():
    """ Получить список задач """
    tasks = getTasks()
    task_list = "\n".join([
        f"{t['id']}: {t['title']} (до {t['deadline']}, {t['priority']})" 
        for t in tasks
    ])
    return task_list

@tool
def getCurrentDateFrom():
    """ Возвращает параметры текущей даты """

    now = datetime.now()

    weekdays_ru = ['понедельник', 'вторник', 'среда', 'четверг', 
        'пятница', 'суббота', 'воскресенье']
    
    return {
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%H:%M"),
        "weekday": weekdays_ru[now.weekday()],
        "datetime": now.strftime("%d-%m-%Y %H:%M")
    }