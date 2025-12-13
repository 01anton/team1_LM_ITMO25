FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY insurance_api.py .

# Копируем модель (убедитесь, что файл существует!)
COPY lgb_model.pkl .

# Выставляем правильные права доступа (важно!)
RUN chmod -R 755 /app && \
    chmod 644 /app/lgb_model.pkl

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 fastapi
USER fastapi

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["uvicorn", "insurance_api:app", "--host", "0.0.0.0", "--port", "5000"]
