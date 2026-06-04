FROM python:3.12-bookworm

# Установка системных зависимостей для сборки bcrypt и других нативных модулей
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Увеличиваем таймауты для pip на случай медленного интернета
RUN pip install --default-timeout=100 --retries 5 --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 4200"]