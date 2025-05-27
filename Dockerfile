FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]