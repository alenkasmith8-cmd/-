import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Union

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


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из JSON файла и возвращает их в виде списка словарей.
    Если файл не существует, возвращает пустой список и выводит сообщение об ошибке.

    :param file_path: Путь к JSON файлу
    :return: Список словарей, содержащих данные из файла
    """
    logger.debug(f'Reading JSON file: {file_path}')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data: Union[List[Dict[str, Any]], Any] = json.load(file)  # Загружаем данные из файла
        # Убедимся, что данные - это список словарей
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            logger.info('Successfully read from JSON file.')
            return data  # Возвращаем считанные данные
        else:
            logger.warning('Data is not a list of dictionaries.')
            return []  # Возврат пустого списка, если данные не соответствуют ожиданиям
    except FileNotFoundError:
        logger.error(f'The file {file_path} does not exist.')
        return []  # Возврат пустого списка, если файл не найден
    except json.JSONDecodeError:
        logger.error(f"Error: The file {file_path} contains invalid JSON.")
        return []  # Возврат пустого списка в случае недопустимого JSON
