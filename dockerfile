# --- Етап 1: Збірка залежностей ---
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Системні пакети для збірки клієнта MariaDB (mysqlclient)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Етап 2: Фінальний легкий образ ---
FROM python:3.12-slim

WORKDIR /app

# Тільки runtime-бібліотека для MariaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Встановлення пакетів з першого етапу
COPY --from=builder /app/wheels /images/wheels
RUN pip install --no-cache /images/wheels/*

# Створення безпечного користувача
RUN useradd -m appuser
COPY --chown=appuser:appuser . .
RUN mkdir -p /app/django_cache && chown -R appuser:appuser /app/django_cache

# Збір статики
RUN SECRET_KEY=temporary_key_for_build python manage.py collectstatic --noinput

# --- ДОДАЙТЕ ЦІ ДВА РЯДКИ ТУТ ---
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Змінюємо CMD на використання entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

