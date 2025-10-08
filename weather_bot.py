import requests
from datetime import datetime

# Настройки
TELEGRAM_BOT_TOKEN = "8354766394:AAFtqM_GjMzgbH-ucERUpOfMThSydPN6_qU"
TELEGRAM_CHAT_ID = "540088380"
OPENWEATHER_API_KEY = "dadb67dd54930dafa659b5491d672c28"  # ЗАМЕНИТЕ!
CITY = "Ижевск"

def get_weather():
    """Получает погоду с OpenWeatherMap"""
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': CITY,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            return f"❌ Ошибка: {data.get('message', 'Город не найден')}"
        
        # Парсим данные
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        
        # Анализ ветра
        if wind_speed < 1:
            wind_analysis = "штиль"
        elif wind_speed < 5:
            wind_analysis = "слабый"
        elif wind_speed < 10:
            wind_analysis = "умеренный"
        elif wind_speed < 15:
            wind_analysis = "сильный"
        else:
            wind_analysis = "очень сильный"
        
        # Анализ давления (норма ~1013 гПа)
        if pressure < 1000:
            pressure_analysis = "низкое"
        elif pressure < 1010:
            pressure_analysis = "пониженное"
        elif pressure < 1020:
            pressure_analysis = "нормальное"
        elif pressure < 1030:
            pressure_analysis = "повышенное"
        else:
            pressure_analysis = "высокое"
        
        # Эмодзи для погоды
        weather_icons = {
            'ясно': '☀️', 'clear': '☀️',
            'облачно': '☁️', 'clouds': '☁️',
            'дождь': '🌧', 'rain': '🌧',
            'снег': '❄️', 'snow': '❄️',
            'туман': '🌫', 'mist': '🌫',
            'гроза': '⛈', 'thunderstorm': '⛈'
        }
        
        icon = '🌤'
        for key, emoji in weather_icons.items():
            if key in description.lower():
                icon = emoji
                break
        
        # Формируем сообщение
        message = (
            f"{icon} Погода в {CITY}\n"
            f"**{description.capitalize()}**\n"
            f"🌡 Температура: {temp:.1f}°C\n"
            f"🤔 Ощущается как: {feels_like:.1f}°C\n"
            f"💨 Ветер: {wind_speed} м/с ({wind_analysis})\n"
            f"🔽 Давление: {pressure} гПа ({pressure_analysis})\n"
            f"💧 Влажность: {humidity}%\n"
            f"\n🕐 {datetime.now().strftime('%H:%M %d.%m.%Y')}"
        )
        
        return message
        
    except Exception as e:
        return f"❌ Ошибка при получении погоды: {str(e)}"

def send_weather():
    """Отправляет погоду в Telegram через простой HTTP запрос"""
    try:
        weather_message = get_weather()
        
        # Отправляем сообщение через HTTP API Telegram (без библиотеки)
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': weather_message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print(f"✅ Уведомление отправлено в {datetime.now().strftime('%H:%M:%S')}")
            return True
        else:
            print(f"❌ Ошибка Telegram API: {response.text}")
            return False
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {str(e)}")
        return False

if __name__ == "__main__":
    send_weather()
