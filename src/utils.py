import json
import os
import typing


def read_json_file(file_path: str) -> typing.List[typing.Dict[str, typing.Any]]:
    """Читает JSON-файл и возвращает список словарей с данными о транзакциях."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            print("Raw data loaded:", data)  # Для отладки
            if isinstance(data, dict) and "transactions" in data:
                return data["transactions"]
            return []
        except json.JSONDecodeError:
            return []
