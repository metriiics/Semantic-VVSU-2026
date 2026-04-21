import sqlite3
from datetime import datetime
from typing import Dict, List

import os

def ini_db() -> None:
    """ Инициализация базы """

    dbPath = os.path.join(os.path.dirname(__file__), 'tasks.db')
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists tasks (
            id integer primary key autoincrement,
            title text unique,
            date text,
            deadline text,
            priority text
        );        
    ''')
    conn.commit()
    conn.close()

def addTask(title: str, date: str, deadline: str, 
            priority: str) -> tuple[bool, str]:
    """ Метод для добавления задачи """

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Проверка на существование записи
    cursor.execute(
        "select * from tasks where title = ?",
        (title.strip(), )
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False, f"Задача с заголовком '{title}' уже заведена!"

    cursor.execute(
        "insert into tasks (title, date, deadline, priority) values (?, ?, ?, ?)",
        (title, date, deadline, priority)
    )
    conn.commit()
    conn.close()
    return True, f"Задача '{title}' добавлена"

def getTasks() -> List[Dict]:
    """ Метод для получения задач """

    conn = sqlite3.connect('tasks.db')
    query = "select * from tasks"

    cursor = conn.execute(query)
    tasks = [{"id": row[0], "title": row[1],
        "date": row[2], "deadline": row[3], "priority": row[4]} 
        for row in cursor.fetchall()
    ]

    conn.close()
    return tasks

def delTasks(title: str) -> tuple[bool, str]:
    """ Метод для удаления задачи """

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM tasks WHERE title = ?", (title.strip(),))
    task = cursor.fetchone()

    if not task:
        conn.close()
        return False, "Задача не найдена"

    cursor.execute("DELETE FROM tasks WHERE title = ?", (title.strip(),))
    conn.commit()

    conn.close()
    return True, f"Задача '{task[1]}' удалена"