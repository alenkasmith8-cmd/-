import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List

# Создаем директорию для логов
os.makedirs('logs', exist_ok=True)

# Создаем объект логгера
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Настроим обработчик для записи логов в файл
file_handler = logging.FileHandler('logs/utils.log')
file_handler.setLevel(logging.DEBUG)

# Определяем формат логирования
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            transactions = json.load(file)
            if isinstance(transactions, list):
                return transactions
            return []  # Вернуть пустой список, если данные не являются списком
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Вернуть пустой список в случае ошибок
