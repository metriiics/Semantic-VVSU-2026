import os

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from dotenv import load_dotenv
load_dotenv()

DBI_URI = os.getenv("MEM")

class MemoryManager:
    def __init__(self):
        self.checkpointer_cm = None
        self.checkpointer = None

    async def connect(self):
        self.checkpointer_cm = (
            AsyncPostgresSaver.from_conn_string(DBI_URI)
        )

        self.checkpointer = (
            await self.checkpointer_cm.__aenter__()
        )

        await self.checkpointer.setup()

    async def close(self):
        if self.checkpointer_cm:
            await self.checkpointer_cm.__aexit__(None, None, None)

memory = MemoryManager()