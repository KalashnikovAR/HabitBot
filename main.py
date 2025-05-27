import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from database import init_db, get_db
from config import BOT_TOKEN

# Инициализация бота с проверкой
if not BOT_TOKEN:
    print("ОШИБКА: Токен бота не задан!")
    exit(1)

bot = os.getenv('BOT_TOKEN')
# Настройка логов
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        init_db()
        await message.answer(
            "⚡ <b>Привет! Я PowerHabitBot!</b>\n\n"
            "Доступные команды:\n"
            "/habits - Управление привычками\n"
            "/todo - Список задач"
        )
    except Exception as e:
        await message.answer("⚠️ Ошибка при запуске бота")
        logging.error(f"Start error: {e}")

# --- Привычки ---
@dp.message(Command("habits"))
async def handle_habits(message: types.Message):
    try:
        args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        user_id = message.from_user.id

        if not args:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT habit, streak FROM habits WHERE user_id = %s", (user_id,))
                    habits = cur.fetchall()

            if not habits:
                await message.answer("Нет привычек. Добавь: /habits + Читать")
            else:
                text = "📌 <b>Твои привычки:</b>\n" + "\n".join(
                    f"• {h['habit']} (🔥 {h['streak']} дн.)" for h in habits
                )
                await message.answer(text)

        elif args.startswith("+"):
            habit = args[1:].strip()
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO habits (user_id, habit) VALUES (%s, %s)", (user_id, habit))
                    conn.commit()
            await message.answer(f"✅ Привычка добавлена: <b>{habit}</b>")

        elif args.startswith("-"):
            habit = args[1:].strip()
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM habits WHERE user_id = %s AND habit = %s", (user_id, habit))
                    conn.commit()
            await message.answer(f"❌ Привычка удалена: <b>{habit}</b>")

        else:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE habits 
                        SET streak = streak + 1, last_completed = CURRENT_DATE 
                        WHERE user_id = %s AND habit = %s
                        AND (last_completed IS NULL OR last_completed < CURRENT_DATE)
                        RETURNING streak
                    """, (user_id, args.strip()))
                    result = cur.fetchone()
                    conn.commit()

            if not result:
                await message.answer("⚠️ Уже выполнено сегодня или привычка не найдена!")
            else:
                await message.answer(f"🔥 <b>+1 день!</b> Текущий стрик: <b>{result[0]}</b> дней")

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при обработке команды")
        logging.error(f"Habits error: {e}")

# --- Задачи ---
@dp.message(Command("todo"))
async def handle_todo(message: types.Message):
    try:
        args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        user_id = message.from_user.id

        if not args:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, task FROM tasks WHERE user_id = %s AND done = FALSE", (user_id,))
                    tasks = cur.fetchall()

            if not tasks:
                await message.answer("📭 Список задач пуст. Добавь: /todo + Купить хлеб")
            else:
                text = "📝 <b>Твои задачи:</b>\n" + "\n".join(
                    f"{i}. {t['task']}" for i, t in enumerate(tasks, 1)
                )
                await message.answer(text)

        elif args.startswith("+"):
            task = args[1:].strip()
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO tasks (user_id, task) VALUES (%s, %s)", (user_id, task))
                    conn.commit()
            await message.answer(f"📌 Задача добавлена: <b>{task}</b>")

        elif args.startswith("-"):
            task_id = args[1:].strip()
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM tasks WHERE user_id = %s AND id = %s", (user_id, task_id))
                    conn.commit()
            await message.answer(f"🗑 Задача <b>{task_id}</b> удалена")

        elif args.startswith("✓") or args.startswith("v"):
            task_id = args[1:].strip()
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE tasks SET done = TRUE WHERE user_id = %s AND id = %s", (user_id, task_id))
                    conn.commit()
            await message.answer(f"✅ Задача <b>{task_id}</b> выполнена!")

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при обработке команды")
        logging.error(f"Todo error: {e}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
