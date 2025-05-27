import os
from dotenv import load_dotenv

# Загрузка токена из .env (если файл есть)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "ваш_токен_вручную"  # Пример: "123456:ABC-DEF123"