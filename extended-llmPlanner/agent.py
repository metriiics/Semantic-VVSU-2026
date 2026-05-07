import sys
import os
import asyncio
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Any
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from skills import detect_skills, build_system_prompt
load_dotenv()

llm = ChatGroq(
    model='llama-3.3-70b-versatile', 
    temperature=0,
    api_key=os.getenv('GROQ_API_KEY')
)

class AgentResponse(BaseModel):
    action: str
    success: bool
    message: str
    data: dict[str, Any] | None = None

client = MultiServerMCPClient(
    {
        "planner": {
            "command":sys.executable,
            "args": ["server.py"],
            "transport": "stdio"
        }
    }
)

form_llm = llm.with_structured_output(
    AgentResponse
)

tools = asyncio.run(client.get_tools())
agent = create_agent(
    model=llm, 
    tools=tools,
)

def ask_agent(question):
    active_skills = detect_skills(question)
    system_prompt = build_system_prompt(active_skills)

    result = asyncio.run(
        agent.ainvoke(
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=question)
                ]
            }
        )
    )

    raw = result["messages"][-1].content
    structed = form_llm.invoke(
        f"""
            Преобразуй ответ ассистента в структуру
            Ответ: {raw}
        """
    )
    return structed