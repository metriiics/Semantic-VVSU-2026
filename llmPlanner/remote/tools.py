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
    """ 
        Add a new task.

        Use when:
        - user wants to create/add a task
        - user agrees to save a planned activity

        Parameters:
        - title: task name
        - date: creation date (DD-MM-YYYY)
        - deadline: due date (DD-MM-YYYY)
        - priority: "высокий", "средний", "низкий"

        Rules:
        - if priority is missing → use "средний"
        - if date is missing → use current date
        - if deadline is missing → use date

        IMPORTANT:
        - normalize date before calling
    """

    success, message = addTask(title, date, deadline, priority)
    return f"{'V' if success else 'X'} {message}"

@tool
def getTasksListTool() -> str:
    """ 
        Get list of all tasks.

        Use when:
        - user asks what tasks they have
        - user asks about schedule or plans

        Returns:
        formatted list of tasks with deadline and priority
    """

    tasks = getTasks()
    task_list = "\n".join([
        f"{t['id']}: {t['title']} (до {t['deadline']}, {t['priority']})" 
        for t in tasks
    ])
    return task_list

@tool
def getCurrentDateFrom() -> Dict:
    """ 
        Get current date and time.

        CRITICAL TOOL.

        MUST be used when user mentions:
        - today / сегодня
        - tomorrow / завтра
        - day after tomorrow / послезавтра
        - in N days / через N дней
        - weekdays (e.g. Friday / пятница)

        DO NOT:
        - guess dates
        - calculate dates without this tool

        Returns:
        {
            "date": "DD-MM-YYYY",
            "time": "HH:MM",
            "weekday": "string",
            "datetime": "DD-MM-YYYY HH:MM"
        }
    """

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
    """ 
        Delete a task by exact title.

        Use when:
        - user wants to remove/delete a task

        IMPORTANT:
        - title must match exactly
    """

    success, message = delTasks(title)
    return f"{'V' if success else 'X'} {message}"

@tool
def getWeather(city: str, date: str) -> str:
    """ 
        Get weather forecast for a specific city and date.

        Use this tool when:
        - user asks about weather
        - user plans outdoor activity (walk, park, picnic)

        Requirements:
        - city MUST be in English (e.g. Moscow, Vladivostok)
        - date MUST be in format DD-MM-YYYY

        IMPORTANT:
        - always normalize date BEFORE calling this tool
        - if user gives relative date → first use getCurrentDateFrom

        Returns:
        weather description and temperature
    """

    api_key = os.getenv("API_WEATHER")

    date_obj = datetime.strptime(date, "%d-%m-%Y")
    search_date = date_obj.strftime("%Y-%m-%d")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code != 200:
        return "Не удалось получить прогноз погоды"

    data = response.json()

    # На нужную дату
    for forecast in data["list"]:
        forecast_date = forecast["dt_txt"].split()[0] 
        if search_date == forecast_date:
            weather = forecast['weather'][0]['description']
            temp = forecast['main']['temp']
            return f"Прогноз в {city} на {date}: {weather}, температура {temp}°C"