#!/bin/sh

# 1. Виправляємо права на змонтовану папку кешу
chown -R appuser:appuser /app/django_cache

# 2. Очікуємо на повну готовність MariaDB за допомогою чистого Python
echo "Waiting for MariaDB..."
python -c '
import socket
import time

while True:
    try:
        with socket.create_connection(("db", 3306), timeout=1):
            print("MariaDB is up and accepting connections!")
            break
    except OSError:
        time.sleep(1)
'

# 3. Виконуємо міграції бази даних
echo "Running database migrations..."
python manage.py migrate

# 4. Запускаємо Gunicorn від імені appuser
echo "Starting Gunicorn server..."
exec gunicorn clientsmanag.wsgi:application --bind 0.0.0.0:8000 --workers 3 --user appuser --group appuser
