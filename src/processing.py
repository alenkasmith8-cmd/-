from typing import Dict, List


def filter_by_state(items: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:

    """ Функция фильтрует список словарей по значению ключа 'state'.
    :param items:Список словарей которые необходимо отфильтровать.
    :param state: Значение по которому будет произведена фильтрация.
    :return: Новый список словарей содержащий только те у которых
     значение ключа 'state', соответствует переданному.
    """

    return [item for item in items if item.get('state') == state]


def sort_by_date(items: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:

    """
    Сортирует список словарей по дате.

    :param items: Список словарей, содержащих информацию с датами.
    :return: Новый список отсортированных словарей по ключу 'date'.
    """

    return sorted(items, key=lambda x: x['date'], reverse=reverse)
