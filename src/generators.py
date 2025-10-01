from typing import Any
from typing import Dict
from typing import Generator
from typing import List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency_code: str
) -> Generator[Dict[str, Any], None, None]:
    """Генератор, который возвращает транзакции с заданной валютой."""
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Генератор, который возвращает описание каждой транзакции."""
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, end + 1):
        formatted_number = f"{number:016d}"  # Форматируем число, добавляя нули спереди
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
