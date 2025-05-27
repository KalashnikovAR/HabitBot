import os

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ОШИБКА: Токен бота не найден!")
    print("ℹ️ Добавьте переменную BOT_TOKEN в настройках Railway")
    exit(1)