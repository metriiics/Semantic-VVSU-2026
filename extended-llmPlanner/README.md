# AI Planner Agent (MCP + LangGraph + Multi-Agent Architecture)

Интеллектуальный AI-планировщик задач с поддержкой:

- MCP (Model Context Protocol)
- multi-agent orchestration
- memory persistence
- subagents
- tool routing
- weather analysis
- task management
- structured AI responses

# Architecture

```bash
Client
  ↓
FastAPI
  ↓
Main Agent (LangGraph)
  ├── Skill Detection
  ├── Prompt Orchestration
  ├── MCP Tool Calling
  ├── Memory Checkpointing
  └── SubAgent Delegation
          ↓
      Weather SubAgent
```

# Основные артефакты и технологии
*MCP*
Что реализовано:
- MCP server 
- MCP tool 
- MCP resources
- stdio transport
- tool orchestration через MCP client

*LangGraph*
Что реализовано:
- state management
- message trimming
- persistence
- middleware execution

*LangChain Agents*
Используется для:
- tool calling
- orchestration
- structured output

*Weather SubAgent*
Специализированный агент для:
- weather analysis
- activity recommendations
- forecast interpretation

*Skill Detection*
RapidFuzz: Mini-NLP-router для определения активных skills
Algo:
- Разбивает строки на токены
- Нормализует
- Ищет пересечение token sets(similarity)

*PostgreSQL*
Используется для:
- task storage
- agent memory
- checkpoint persistence

*SQLAlchemy ORM*
Реализовано:
- declarative models
- CRUD abstraction
- session factory
- transactional operations

*LangGraph Checkpoint Memory*
Возможности:
- persistent conversations
- thread state recovery
- long-term execution memory

*Message History Management*
Используется:
- control context window
- prevent token overflow
- trimming

*Fast API Layer*

# Managment database

`\dt` - просмотр таблиц \
`\l` - просмотр баз \
`\c planner` - подключиться к базе \
`\d tasks` - просмотр таблицы в базе