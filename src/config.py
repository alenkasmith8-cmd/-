# src/config.py
import os
from pathlib import Path

# Определяем корневую директорию проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Путь к директории с данными
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# Путь к директории с логами
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)  # Создаем директорию для логов, если она не существует

# Файл логов
LOG_FILE = os.path.join(LOG_DIR, 'app.log')


# Настройки логирования
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'filename': LOG_FILE,
}

# Получаем путь к базовой директории проекта


BASE_DIR: Path = Path(__file__).resolve().parent.parent  # Это указывает на директорию project/
DATA_DIR = BASE_DIR / 'data'
