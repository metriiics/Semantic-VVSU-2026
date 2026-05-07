import asyncio
from agent import ask_agent
from datebase.crud import DBaseQuery

result = ask_agent("Какие у меня есть задачи?")
print(result.message)
print(result.data)