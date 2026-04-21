from langchain_core.tools import tool
from db import addTask, getTasks, delTasks
from datetime import datetime
from typing import Dict
import requests
from dotenv import load_dotenv
import os

load_dotenv()

@tool
def addTaskTool(title: str, date: str, deadline: str, 
            priority: str) -> str:
    """ Добавить задачу """

    success, message = addTask(title, date, deadline, priority)
    return f"{'V' if success else 'X'} {message}"

@tool
def getTasksListTool() -> str:
    """ Получить список задач """

    tasks = getTasks()
    task_list = "\n".join([
        f"{t['id']}: {t['title']} (до {t['deadline']}, {t['priority']})" 
        for t in tasks
    ])
    return task_list

@tool
def getCurrentDateFrom() -> Dict:
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

@tool
def delTaskTool(title: str) -> str:
    """ Удаление задачи """

    success, message = delTasks(title)
    return f"{'V' if success else 'X'} {message}"

@tool
def getWeather(city: str, date: str = 'сегодня'):
    """ Получение прогноза погоды для планирования активностей """

    api_key = os.getenv("API_WEATHER")

    date_obj = datetime.strptime(date, "%d-%m-%Y")
    search_date = date_obj.strftime("%Y-%m-%d")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    # На нужную дату
    for forecast in data["list"]:
        forecast_date = forecast["dt_txt"].split()[0] 
        if search_date == forecast_date:
            weather = forecast['weather'][0]['description']
            temp = forecast['main']['temp']
            return f"Прогноз в {city} на {date}: {weather}, температура {temp}°C"