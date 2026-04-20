from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from agent import agent
from db import ini_db

class GenerateRequest(BaseModel):
    quest: str

app = FastAPI(
    title="Local LLM Planner",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startupEvent():
    """ Инициализация при запуске программы """
    ini_db()

@app.get("/health")
async def healthCheck():
    """ Проверка состояния API """

    return "Ok!"

@app.post("/generate")
async def generate(request: GenerateRequest):
    response = agent.invoke({"messages": [("user", request.quest)]})
    return response["messages"][-1].content

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )