import asyncio
from agent import ask_agent

async def test_agent():
    result = await ask_agent("Создай заметку имя - помыть, статус -срений")
    print(result)

asyncio.run(test_agent())