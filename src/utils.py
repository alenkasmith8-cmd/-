import json
from typing import Any
from typing import Dict
from typing import List
from typing import Union


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из JSON файла и возвращает их в виде списка словарей.
    Если файл не существует, возвращает пустой список и выводит сообщение об ошибке.

    :param file_path: Путь к JSON файлу
    :return: Список словарей, содержащих данные из файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data: Union[List[Dict[str, Any]], Any] = json.load(file)  # Загружаем данные из файла
        # Убедимся, что данные - это список словарей
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return data  # Возвращаем считанные данные
        else:
            print(f"Warning: The data in {file_path} is not a list of dictionaries.")
            return []  # Возврат пустого списка, если данные не соответствуют ожиданиям
    except FileNotFoundError:
        print(f"Warning: The file {file_path} does not exist.")
        return []  # Возврат пустого списка, если файл не найден
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return []  # Возврат пустого списка в случае недопустимого JSON
