from typing import List, Dict, Tuple
from rapidfuzz import fuzz
from textwrap import dedent

SYSTEM_PROMPT: str = "Ты умный AI-ассистент для планирования задач и активностей."

SKILLS: List[Dict[str, str]] = [
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
            Основные правила при работе с базой данных:
                Определяй намерение пользователя:
                    - создать задачу
                    - обновить задачу
                    - удалить задачу
                    - посмотреть задачи
                    - изменить статус
                    - найти задачу

                - Всегда извлекай:
                    - название задачи
                    - дату или дедлайн
                    - статус задачи (если указан)

                - Если данных недостаточно:
                    - задай уточняющий вопрос.

                - При создании задачи:
                    - подтверждай успешное создание.

                - При удалении:
                    - сообщай результат операции.

                - При обновлении:
                    - показывай измененные данные.

                Формат ответа:
                - короткий
                - структурированный
                - без лишнего текста

                Никогда:
                - не придумывай ID задач
                - не изменяй данные без подтвержденного намерения
                - не- удаляй задачи без явного запроса пользователя
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

def ratio_skills(query: str) -> List[Tuple[str, float]]:
    result: List = []
    query_lower: str = query.lower()
    
    for skill in SKILLS:
        ratio: List = []
        name: str = skill.get('skill')
        keywords: str = skill.get('keywords')
        for item in keywords:
            score: int = fuzz.token_set_ratio(query_lower, item)
            ratio.append(score)
        max_ratio: int = max(ratio)
        result.append((name, max_ratio))
    return result

def detect_skills(query: str) -> List[str]:
    bound: int = 51
    probability: List[Tuple[str, float]] = ratio_skills(query)
    name_skills: List[str] = [item[0] for item in probability if item[1] >= bound]
    if not name_skills:
        return None
    return name_skills

def build_system_prompt(skills: List[str]) -> str:
    parts: List[str] = [SYSTEM_PROMPT]

    if skills is None:
        return SYSTEM_PROMPT

    for skill in SKILLS:
        if skill.get("skill") in skills:
            rule: str = dedent(
                skill.get("rule")
            ).strip()
            parts.append(rule)
    return "\n\n".join(parts)