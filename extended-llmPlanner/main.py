from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from agent.agent import ask_agent
from database.crud import DBaseQuery
from agent.serialize import AgentResponse
from database.memory import memory

@asynccontextmanager
async def lifespan(app: FastAPI):

    DBaseQuery.create_tables()

    await memory.connect()

    yield

    await memory.close()

app = FastAPI(
    title="Agent Planner", 
    lifespan=lifespan
)

@app.post("/api/v1/ask", response_model=AgentResponse)
async def main(query: str) -> AgentResponse:
    result = await ask_agent(query)

    return result

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )