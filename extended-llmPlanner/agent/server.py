from mcp.server.fastmcp import FastMCP

from datetime import datetime

from agent.serialize import Task
from database.crud import DBaseQuery

from typing import Dict

mcp = FastMCP('Demo')

@mcp.tool()
def tool_create_task(task: Task):
    """
        Create a new task in the database.

        Args:
            task (Task):
                Task data containing:
                - name (str): Task title
                - date (datetime | None): Task date
                - status (str): Current task status

        Returns:
            dict:
                Created task information:
                - id (int)
                - name (str)
                - status (str)
    """
    return DBaseQuery.create_task(task)

@mcp.tool()
def tool_read_task():
    """
        Retrieve all tasks from the database.

        Returns:
            list[dict]:
                List of tasks with:
                - id (int)
                - name (str)
                - status (str)
    """
    tasks = DBaseQuery.read_task()
    return tasks

@mcp.tool()
def tool_read_task_id(task_id):
    """ 
        Retrieve a task by its ID.

        Args:
            task_id (int):
                Unique task identifier.

        Returns:
            dict:
                Task information:
                - id (int)
                - name (str)
                - status (str)

            or

            dict:
                Error message if task does not exist.
    """
    return DBaseQuery.read_task_id(task_id)

@mcp.tool()
def tool_update_task(task_id, name):
    """ 
        Update task name by task ID.

        Args:
            task_id (int):
                Unique task identifier.

            name (str):
                New task name.

        Returns:
            dict:
                Updated task information:
                - id (int)
                - name (str)
                - status (str)

            or

            dict:
                Error message if task does not exist.
    """
    return DBaseQuery.update_task(task_id, name)

@mcp.tool()
def tool_delete_task(task_id):
    """ 
        Delete a task from the database by ID.

        Args:
            task_id (int):
                Unique task identifier.

        Returns:
            dict:
                Deleted task information:
                - id (int)
                - name (str)
                - status (str)

            or

            dict:
                Error message if task does not exist.
    """
    return DBaseQuery.delete_task(task_id)

@mcp.tool()
def tool_curr_date() -> Dict[str, str]:
    """
        Retrieve the current local date and time information.

        This tool is the single source of truth for all date and time operations
        inside the agent system. The agent must use this tool whenever it needs
        to interpret relative dates such as:
        - today
        - tomorrow
        - next Monday
        - in a week
        - this evening
    """
    now = datetime.now()

    week_days_ru = ['понедельник', 'вторник', 'среда', 'четверг', 
        'пятница', 'суббота', 'воскресенье']
   
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H:%M")
    weekday = week_days_ru[now.weekday()]
    curr_datetime = now.strftime("%d.%m.%Y %H:%M:%S")

    formular = {
        "date": date,
        "time": time,
        "weekday": weekday,
        "datetime": curr_datetime 
    }

    return formular

@mcp.resource("resource://timezone")
def timezone():
    tz = datetime.now().astimezone().tzinfo
    return {
        "timezone": str(tz)
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")