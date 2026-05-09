import os
from dotenv import load_dotenv
from datetime import datetime
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool

load_dotenv()

subAgent = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY1")
)

@tool
def get_curr_weather(city: str, date: str) -> str:
    """ 
        Get weather forecast for a specific city and date.

        Use this tool when:
        - user asks about weather
        - user plans outdoor activity (walk, park, picnic)

        Requirements:
        - city MUST be in English (e.g. Moscow, Vladivostok)
        - date MUST be in format DD-MM-YYYY

        IMPORTANT:
        - always normalize date BEFORE calling this tool
        - if user gives relative date → first use getCurrentDateFrom

        Returns:
        weather description and temperature
    """
    api_key = os.getenv("API_WEATHER")

    date_obj = datetime.strptime(date, "%d-%m-%Y")
    search_date = date_obj.strftime("%Y-%m-%d")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code != 200:
        return "Не удалось получить прогноз погоды"

    data = response.json()

    for forecast in data["list"]:
        forecast_date = forecast["dt_txt"].split()[0] 
        if search_date == forecast_date:
            weather = forecast['weather'][0]['description']
            temp = forecast['main']['temp']
            return f"Прогноз в {city} на {date}: {weather}, температура {temp}°C"

SYSTEM_PROMPT_SUBAGENT = """
    You are a weather analysis subagent.

    Your responsibilities:

    analyze weather conditions
    interpret the forecast
    provide activity recommendations

    Rules:

    Use only the provided weather data.
    Do not invent weather conditions.
    Analyze:
    temperature
    precipitation
    wind
    overall comfort of conditions
    For outdoor activities:
    assess weather suitability
    warn about risks
    suggest alternatives in bad weather
    Respond:
    informatively
    without unnecessary text
"""