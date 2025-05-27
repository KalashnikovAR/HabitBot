from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN
from database import init_db
import asyncio
import os

bot = os.getenv("BOT_TOKEN")
dp = Dispatcher()

# Инициализация БД при старте
init_db()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("⚡ Бот запущен на Railway!")

# --- Привычки ---
@dp.message(Command("habits"))
async def habits(message: types.Message):
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    user_id = message.from_user.id

    if not args:
        habits_list = get_habits(user_id)
        if not habits_list:
            await message.answer("Нет привычек. Добавь: /habits + Читать")
        else:
            text = "Твои привычки:\n" + "\n".join(f"• {h} (🔥 {s} дн.)" for h, s in habits_list)
            await message.answer(text)

    elif args.startswith("+"):
        habit = args[1:].strip()
        add_habit(user_id, habit)
        await message.answer(f"Привычка добавлена: {habit}")

    elif args.startswith("-"):
        habit = args[1:].strip()
        delete_habit(user_id, habit)
        await message.answer(f"Привычка удалена: {habit}")

    else:
        streak = complete_habit(user_id, args)
        if streak == -1:
            await message.answer("Уже выполнено сегодня!")
        else:
            await message.answer(f"🔥 Streak: {streak} дней!")


# --- Задачи ---
@dp.message(Command("todo"))
async def todo(message: types.Message):
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    user_id = message.from_user.id

    if not args:
        tasks = get_tasks(user_id)
        if not tasks:
            await message.answer("Нет задач. Добавь: /todo + Купить хлеб")
        else:
            text = "Твои задачи:\n" + "\n".join(f"{i}. {task}" for i, task in tasks)
            await message.answer(text)

    elif args.startswith("+"):
        task = args[1:].strip()
        add_task(user_id, task)
        await message.answer(f"Задача добавлена: {task}")

    elif args.startswith("-"):
        task_id = args[1:].strip()
        delete_task(user_id, task_id)
        await message.answer(f"Задача {task_id} удалена")

    elif args.startswith("✓"):
        task_id = args[1:].strip()
        complete_task(user_id, task_id)
        await message.answer(f"✅ Задача {task_id} выполнена!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())