import os
from dotenv import load_dotenv
from typing import List

from agent.serialize import AgentResponse
from agent.skills import detect_skills, build_system_prompt
from database.memory import memory
from agent.subagent import subAgent, SYSTEM_PROMPT_SUBAGENT, get_curr_weather

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents.middleware.subagents import SubAgentMiddleware

load_dotenv()

llm = ChatGroq(
    model='llama-3.3-70b-versatile', 
    temperature=0,
    api_key=os.getenv('GROQ_API_KEY')
)

async def ask_agent(question) -> AgentResponse:
    active_skills: List[str] = detect_skills(question)
    system_prompt: str = build_system_prompt(active_skills)

    client = MultiServerMCPClient(
        {
            "planner": {
                "command": "python3.14",
                "args": ["-m", "agent.server"],
                "transport": "stdio"
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(
        model=llm, 
        tools=tools,
        response_format=AgentResponse,
        checkpointer=memory.checkpointer,
        middleware=[
            SubAgentMiddleware(
                backend=llm,
                subagents=[
                    {
                        "name": "weather",
                        "description": "This subagents can get and analisys weather in cities",
                        "system_prompt": SYSTEM_PROMPT_SUBAGENT,
                        "tools": [get_curr_weather],
                        "model": subAgent,
                        "middleware": [],
                    }
                ]
            )
        ]
    )

    result = await agent.ainvoke(
        {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]
        },
        config={
            "configurable": {
                "thread_id": "user_123"
            }
        }
    )
    resp = result["structured_response"]
    return resp