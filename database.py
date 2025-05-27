import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

def get_db():
    """Подключение к PostgreSQL"""
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    return conn

def init_db():
    """Инициализация таблиц"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS habits (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            habit TEXT NOT NULL,
            streak INTEGER DEFAULT 0,
            last_completed DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
        """
    )
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        if conn is not None:
            conn.close()

# ... остальные функции (аналогично SQLite, но с синтаксисом PostgreSQL) ...