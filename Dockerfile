# Базовый образ
FROM python:3.11-slim

# Установка зависимостей для PostgreSQL
RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Настройка окружения
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Рабочая директория
WORKDIR /app

# Копирование файлов
COPY requirements.txt .
COPY *.py .

# Установка Python-зависимостей
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Запуск бота
CMD ["python", "main.py"]