def filter_by_state(data, state ='EXECUTED'):
    """Функция фильтрует список словарей по значению ключа 'state'"""
    return [item for item in data if item['state']==state]


def sort_by_date(data, descending = True):
    """Функция сортирует список словарей по ключу 'date'"""
    return sorted(data, key = lambda x: x['date'], reverse= descending)