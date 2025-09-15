from typing import Dict
from typing import List


def filter_by_state(data: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """Функция фильтрует список словарей по значению ключа 'state'
    :param data:Список словарей с бакновскими операциями.
    :param state: Значение для ключа 'state', по умолчанию 'EXECUTED'.
    :return: Новый список словарей с совпадающим состоянием.
    """

    return [item for item in data if item['state'] == state]


def sort_by_date(data: List[Dict], descending: bool = True) -> List[Dict]:
    """Функция сортирует список словарей по ключу 'date'
    :param data: Список словарей с банковскими операциияями.
    :param descending: Порядок сортировки, по умолчанию по убыванию.
    :return: Новый список словарей, отсортированный по дате.
    """

    return sorted(data, key=lambda x: x['date'], reverse=descending)
