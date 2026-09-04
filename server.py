from waitress import serve
from clientsmanag.wsgi import application # Replace 'your_project_name'
from dotenv import load_dotenv
import logging
import os
import socket
import signal
import sys


# Коренева директорія застосунку
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Загружаем переменные из файла .env
load_dotenv(os.path.join(BASE_DIR, '.env'))
# Запис логу в файл
LOG_FILE = os.path.join(BASE_DIR, "server_log.txt")

# Зчитуємо нові параметри мережі
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8000"))
WEB_THREADS = int(os.getenv("WEB_THREADS", "6"))

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)
# встановити рівень логування для Waitress на ERROR
logging.getLogger('waitress.queue').setLevel(logging.ERROR)

def handle_shutdown(signum, frame):
    # logger.info(#Записуємо в лог сигнал
    # logging.info(f"Отримано сигнал {signal.Signals(signum).name}. Зупинка серверу...")
    logging.info(f"--- ЗУПИНКА СЕРВЕРУ PYTHON: Отримано сигнал {signal.Signals(signum).name}. ---") 
    # Тут можна закрити з'єднання з БД, якщо потрібно
    sys.exit(0)

# Прив'язуємо обробники до сигналів зупинки
signal.signal(signal.SIGINT, handle_shutdown)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_shutdown)  # Команда kill / Docker stop

# Перевірка чи зайнятий порт який ми хочемо використати.
def is_port_in_use(port, host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # поверне True, якщо порт зайнятий, і False, якщо вільний
        # return s.connect_ex((host, port)) == 0
        try:
            s.bind((host,port))
            return False    # Порт вільний
        except OSError:
            return True     # Помилка порт зайнятий

if __name__ == '__main__':
    try:
        if not all([WEB_HOST, WEB_PORT, WEB_THREADS]):
            raise ValueError("Один або кілька параметрів конфігурації відсутні у файлі .env")
        
        # Проверка и установка значения по умолчанию
        # if not BACKUP_DIR:
        #     BACKUP_DIR = os.path.join(SCRIPT_DIR, "backups")
        
        if WEB_HOST=='localhost':
            WEB_HOST='127.0.0.1'

        # Перевірка чи зайнятий порт який ми хочемо використати.
        if is_port_in_use(WEB_PORT, WEB_HOST):
            raise ValueError(f"Попередження: Порт {WEB_PORT} вже зайнятий!")

        logging.info(f"--- ЗАПУСК СЕРВЕРУ PYTHON: http://{WEB_HOST}:{WEB_PORT} ---") 
        logging.info(f"Поточні налаштування: WEB_THREADS = {WEB_THREADS}") 
        print(f"Serving application on http://{WEB_HOST}:{WEB_PORT} ")  
        # serve(application, host='0.0.0.0', port=8000) # Binds to all interfaces
        # serve(application, host='192.168.1.200', port=8081, threads = 6) # Binds to 192.168.1.200 interface 
        serve(application, host=WEB_HOST, port=WEB_PORT, threads = WEB_THREADS) # Binds to 192.168.1.200 interface 

    except Exception as init_err:
        logging.critical(f"Помилка ініціалізації скрипта: {init_err}")
        print(f"Помилка ініціалізації скрипта: {init_err}")

# if __name__ == '__main__':
#     # Optional: Retrieve port from an environment variable (e.g., for Heroku or IIS)
#     # PORT = os.getenv("PORT", "8000") 
#     print("Serving application...")
#     # serve(application, host='0.0.0.0', port=8080) # Binds to all interfaces
#     serve(application, host='192.168.1.200', port=8585, threads = 6) # Binds to 192.168.1.200 interface
