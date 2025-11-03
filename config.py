from pathlib import Path

# Определяем корневую директорию проекта
BASE_DIR: Path = Path(__file__).resolve().parent.parent  # Указывает на директорию проекта

# Путь к директории с данными
DATA_DIR: Path = BASE_DIR / 'data'

# Путь к директории с логами
LOG_DIR: Path = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Создаем директорию для логов, если она не существует

# Файл логов
LOG_FILE: Path = LOG_DIR / 'app.log'

# Настройки логирования
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'filename': str(LOG_FILE),  # Преобразуем в строку, если необходимо
}
