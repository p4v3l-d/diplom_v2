# Базовый образ с Python
FROM python:3.11-slim

# Не создаём .pyc-файлы и ведём лог прямо в stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /code

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходники проекта
COPY . .

# Команда запуска (production-вариант, без --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
