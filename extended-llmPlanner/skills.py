from typing import List, Dict

SYSTEM_PROMPT: str = ""

SKILLS: Dict[str, str] = {
    "weather": """ [Skill: Работа с погодой] """,
    "date": """ [Skill: Работа с датами] """,
}

SKILLS_KEYWORDS: Dict[str, List[str]] = {
    "weather": ["погода", "прогулка", "солнце", "дождь"],
    "date": ["дата", "время", "число", "завтра"]
}

def detect_skills(query: str):
    query_lower = query.lower()
    return [
        skill 
        for skill, keywords in SKILLS_KEYWORDS.items()
        if any(kw in query_lower for kw in keywords)
    ]

def build_system_prompt(skills):
    parts = [SYSTEM_PROMPT]
    for name in skills:
        if name in skills:
            parts.append(SKILLS[name])
    return "\n\n".join(parts)