import sys
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
load_dotenv()

llm = ChatGroq(
    model='llama-3.1-8b-instant', 
    temperature=0,
    api_key=os.getenv('GROQ_API_KEY')
)

async def ask_agent(question):
    client = MultiServerMCPClient(
        {
            "planner": {
                "command":sys.executable,
                "args": ["APP-MCP.py"],
                "transport": "stdio"
            }
        }    
    )
    tools = await client.get_tools()
    agent = create_agent(
        model=llm, 
        tools=tools,
        system_prompt="""
        Ты AI-ассистент для планирования задач и активностей.
        
        1. Для добавления задач используй tools
        2. После вызова инструмента дай финальный ответ
        """
    )
    result = await agent.ainvoke({"input": question})
    return result["messages"][-1].content

class ResponseFrom():
    pass