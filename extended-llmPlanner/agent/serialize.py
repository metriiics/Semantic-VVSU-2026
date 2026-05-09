from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, List, Optional

class TaskStatus(str, Enum):
    pending: str = 'Записал'
    in_progress: str = 'В процессе'
    done: str = 'Выполнена'

class Task(BaseModel):
    name: str = Field(description="Name task")
    date: Optional[str] = Field(description="Task deadline")
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description="Statuses that can be set for a task, according to the TaskStatus form."
    )

class AgentResponse(BaseModel):
    tools: List[str] = Field(
        default=None,
        description="Tools that the assistant used to respond to the user's request from the set of available tools."
    )
    message: str = Field(
        default=None, 
        description="The assistant's response to the user's request."
    )
    skills: List[str] = Field(
        default=None,
        description="Skills that the assistant used to respond to the user's request from the set of available skills: [weather, task manager, date]"
    )