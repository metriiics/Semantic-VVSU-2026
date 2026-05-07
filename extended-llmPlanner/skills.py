from typing import List, Dict
from rapidfuzz import fuzz
from textwrap import dedent

SYSTEM_PROMPT: str = "Ты умный AI-ассистент для планирования задач и активностей."

SKILLS = [
    {
        "skill": "weather",
        "description": "[Skill: Работа с погодой]",
        "rule": """

                """,
        "keywords": [
            "погода", 
            "прогулка", 
            "пройтись", 
            "прогуляться",
            "активность",
            "пешком"
        ]
    },
    
    {
        "skill": "date",
        "description": "[Skill: Работа с датами]",
        "rule": """
                    Обрабытывай даты будто ты человек мира, 
                    как будто
                    Обрабытывай даты будто ты человек мира, 
                    как будто
                    Обрабытывай даты будто ты человек мира, 
                    как будто
                """,
        "keywords": [
            "дату",
            "дата",
            "завтра",
            "сегодня",
            "воскресенье",
            "понедельник",
            "вторник"
        ]
    },

    {
        "skill": "task_manager",
        "descriptions": "[Skill: Работа с базой данных]",
        "rule": """ 
                rfaljfl
            """,
        "keywords": [
            "задачи", 
            "сделать", 
            "дедлайн?", 
            "todo", 
            "дела",
            "планы"
        ]    
    }
]

query = "Какие у меня задачи на сегодня"

def ratio_skills(query: str):
    result = []
    query_lower = query.lower()
    
    for skill in SKILLS:
        ratio = []
        name = skill.get('skill')
        keywords = skill.get('keywords')
        for item in keywords:
            score = fuzz.token_set_ratio(query_lower, item)
            ratio.append(score)
        max_ratio = max(ratio)
        result.append((name, max_ratio))
    return result

def detect_skills(query: str):
    bound = 51
    probability = ratio_skills(query)
    name_skills = [item[0] for item in probability if item[1] >= bound]
    return name_skills

def build_system_prompt(skills):
    parts = [SYSTEM_PROMPT]
    for skill in SKILLS:
        if skill.get("skill") in skills:
            rule = dedent(
                skill.get("rule")
            ).strip()
            parts.append(rule)
    return "\n\n".join(parts)