import time
import schedule
from datetime import datetime
import requests

# Импортируем функцию из основного файла
from weather_bot import send_weather

def job():
    print(f"🕐 Запуск отправки погоды: {datetime.now()}")
    send_weather()

# Настраиваем расписание (по UTC)
schedule.every().day.at("02:00").do(job)  # 06:00 Ижевск
schedule.every().day.at("09:00").do(job)  # 13:00 Ижевск  
schedule.every().day.at("15:00").do(job)  # 19:00 Ижевск

print("🚀 Планировщик запущен...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Проверяем каждую минуту
