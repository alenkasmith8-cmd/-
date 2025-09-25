from typing import Dict, List
from datetime import datetime


def filter_by_state(items: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    """Функция фильтрует список словарей по значению ключа 'state'."""

    return [item for item in items if item.get('state') == state]


def sort_by_date(items: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует список словарей по дате и id.

    :param items: Список словарей, содержащих информацию с датами.
    :param reverse: Указывает, сортировать ли в обратном порядке.
    :return: Новый список отсортированных словарей по ключам 'date' и 'id'.
    """

    return sorted(items, key=lambda x: (datetime.strptime(x['date'], "%Y-%m-%d"), x['id']), reverse=reverse)
