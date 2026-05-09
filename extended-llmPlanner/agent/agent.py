import os
from dotenv import load_dotenv
from typing import List

from agent.serialize import AgentResponse
from agent.skills import detect_skills, build_system_prompt
from database.memory import memory
from agent.subagent import subAgent, SYSTEM_PROMPT_SUBAGENT, get_curr_weather

from langchain_groq import ChatGroq
from langchain.agents import create_agent, AgentState
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain_core.messages import trim_messages
from langchain.agents.middleware import before_model
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

load_dotenv()

llm = ChatGroq(
    model='qwen/qwen3-32b', 
    temperature=0,
    api_key=os.getenv('GROQ_API_KEY')
)

structed_llm = llm.with_structured_output(AgentResponse)

@before_model
def trim_history(state: AgentState, runtime: Runtime):
    messages = state["messages"]

    trimmed = trim_messages(
        messages,
        strategy="last",
        token_counter=llm,
        max_tokens=2500,
        include_system=True,
        allow_partial=False
    )

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *trimmed
        ]
    }

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
        checkpointer=memory.checkpointer,
        middleware=[
            trim_history,
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
                "thread_id": "user_212313245"
            }
        }
    )

    final_ai_message = next(
        msg
        for msg in reversed(result["messages"])
        if isinstance(msg, AIMessage)
    )

    final_text = final_ai_message.content
    parsed_response = await structed_llm.ainvoke(final_text)
    return parsed_response