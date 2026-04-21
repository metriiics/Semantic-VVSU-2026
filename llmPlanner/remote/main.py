import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_openweathermap():
    api_key = os.getenv("API_WEATHER")
    
    if not api_key:
        print("❌ API ключ не найден в .env файле")
        print("Добавьте OPENWEATHER_API_KEY=ваш_ключ в .env")
        return
    
    # Тестовый запрос текущей погоды
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Moscow",
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    
    print(f"🔍 Тестируем API с городом: Москва")
    print(f"URL: {url}")
    print(f"Параметры: q=Moscow, units=metric, lang=ru")
    print("-" * 50)
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API работает корректно!")
            print(f"\n📊 Полученные данные:")
            print(f"   Город: {data.get('name')}")
            print(f"   Температура: {data['main']['temp']}°C")
            print(f"   Ощущается как: {data['main']['feels_like']}°C")
            print(f"   Погода: {data['weather'][0]['description']}")
            print(f"   Влажность: {data['main']['humidity']}%")
            print(f"   Ветер: {data['wind']['speed']} м/с")
            return True
        elif response.status_code == 401:
            print("❌ Ошибка авторизации: неверный API ключ")
            print("   Проверьте правильность ключа в .env файле")
        elif response.status_code == 404:
            print("❌ Город не найден")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Сообщение: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Таймаут: сервер не отвечает")
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения: проверьте интернет")
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")
    
    return False

def test_forecast():
    """Тест 5-дневного прогноза"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return
    
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": "Moscow",
        "appid": api_key,
        "units": "metric",
        "lang": "ru",
        "cnt": 5  # количество записей
    }
    
    print("\n" + "=" * 50)
    print("🔮 Тестируем 5-дневный прогноз")
    print("-" * 50)
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Прогноз работает!")
            print(f"\n📅 Прогноз на 5 дней (каждые 3 часа):")
            
            for i, forecast in enumerate(data['list'][:3]):  # первые 3 прогноза
                print(f"\n   {i+1}. {forecast['dt_txt']}")
                print(f"      Температура: {forecast['main']['temp']}°C")
                print(f"      Погода: {forecast['weather'][0]['description']}")
        else:
            print(f"❌ Ошибка прогноза: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🧪 ТЕСТИРОВАНИЕ OPENWEATHERMAP API")
    print("=" * 50)
    
    success = test_openweathermap()
    
    if success:
        test_forecast()
        print("\n" + "=" * 50)
        print("✅ API настроен правильно! Можете использовать getWeather в вашем планировщике.")
    else:
        print("\n" + "=" * 50)
        print("⚠️ API не работает. Проверьте:")
        print("1. Корректность API ключа в .env файле")
        print("2. Подключение к интернету")
        print("3. Не превышен ли лимит запросов (1000/день для бесплатного тарифа)")