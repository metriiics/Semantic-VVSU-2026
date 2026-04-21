from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from agent import agent
from db import ini_db

chat_history = []

class GenerateRequest(BaseModel):
    quest: str

class GenerateResponse(BaseModel):
    resp: str

class HealthCheckResponse(BaseModel):
    status: str

app = FastAPI(
    title="Remote LLM Planner",
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

@app.get("/health", response_model=HealthCheckResponse)
async def healthCheck():
    """ Проверка состояния API """

    return HealthCheckResponse(status="Ok!")

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """ Возвращает ответ модели """
    global chat_history

    messages = []

    for msg in chat_history[-6:]:
        messages.append(msg)

    messages.append(("user", request.quest))

    response = agent.invoke({"messages": messages})
    answer = response["messages"][-1].content

    chat_history.append(("user", request.quest))
    chat_history.append(("assistant", answer))

    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    return GenerateResponse(resp=answer)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )