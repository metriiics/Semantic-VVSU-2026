import asyncio
from agent import ask_agent

async def test_agent():
    result = await ask_agent("Какие у меня есть задачи?")
    print(result)

asyncio.run(test_agent())