import os
from dotenv import load_dotenv

load_dotenv()

# Проверка токена перед использованием
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден! Проверьте .env или переменные окружения")