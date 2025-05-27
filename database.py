import sqlite3
from datetime import datetime


def get_db():
    """Подключение к базе данных SQLite."""
    return sqlite3.connect("prod.db")


def init_db():
    """Создание таблиц, если они не существуют."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS habits (user_id INTEGER, habit TEXT, streak INTEGER DEFAULT 0, last_completed TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (user_id INTEGER, task TEXT, done BOOLEAN DEFAULT 0)")
    conn.commit()


# --- Функции для привычек ---
def add_habit(user_id: int, habit: str):
    conn = get_db()
    conn.execute("INSERT INTO habits (user_id, habit) VALUES (?, ?)", (user_id, habit))
    conn.commit()


def delete_habit(user_id: int, habit: str):
    conn = get_db()
    conn.execute("DELETE FROM habits WHERE user_id = ? AND habit = ?", (user_id, habit))
    conn.commit()


def complete_habit(user_id: int, habit: str) -> int:
    conn = get_db()
    today = datetime.now().strftime("%Y-%m-%d")

    cursor = conn.cursor()
    cursor.execute("SELECT last_completed FROM habits WHERE user_id = ? AND habit = ?", (user_id, habit))
    result = cursor.fetchone()

    if result and result[0] == today:
        return -1

    cursor.execute("UPDATE habits SET streak = streak + 1, last_completed = ? WHERE user_id = ? AND habit = ?",
                   (today, user_id, habit))
    conn.commit()

    cursor.execute("SELECT streak FROM habits WHERE user_id = ? AND habit = ?", (user_id, habit))
    return cursor.fetchone()[0]


def get_habits(user_id: int) -> list[tuple[str, int]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT habit, streak FROM habits WHERE user_id = ?", (user_id,))
    return cursor.fetchall()


# --- Функции для задач ---
def add_task(user_id: int, task: str):
    conn = get_db()
    conn.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (user_id, task))
    conn.commit()


def delete_task(user_id: int, task_id: int):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE user_id = ? AND rowid = ?", (user_id, task_id))
    conn.commit()


def complete_task(user_id: int, task_id: int):
    conn = get_db()
    conn.execute("UPDATE tasks SET done = 1 WHERE user_id = ? AND rowid = ?", (user_id, task_id))
    conn.commit()


def get_tasks(user_id: int) -> list[tuple[int, str]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, task FROM tasks WHERE user_id = ? AND done = 0", (user_id,))
    return cursor.fetchall()