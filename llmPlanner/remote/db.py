import sqlite3
from datetime import datetime
from typing import Dict, List

import os

def ini_db() -> None:
    dbPath = os.path.join(os.path.dirname(__file__), 'tasks.db')
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists tasks (
            id integer primary key,
            title text,
            date text,
            deadline text,
            priority text
        );        
    ''')
    conn.commit()
    conn.close()

def addTask(title: str, date: str, deadline: str, 
            priority: str) -> None:
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "insert into tasks (title, date, deadline, priority) values (?, ?, ?, ?)",
        (title, datetime.now(), deadline, priority)
    )
    conn.commit()
    conn.close()

def getTasks() -> List[Dict]:
    conn = sqlite3.connect('tasks.db')
    query = "select * from tasks"

    cursor = conn.execute(query)
    tasks = [{"id": row[0], "title": row[1],
        "date": row[3], "deadline": row[4], "priority": row[5]} 
        for row in cursor.fetchall()
    ]

    conn.close()
    return tasks