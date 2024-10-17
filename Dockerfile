FROM python:3.12.2

# Устанавливаем необходимые пакеты
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]