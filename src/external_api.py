import os
from typing import Any
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env


def get_exchange_rate(currency: str) -> float:
    """Получает курс валюты по отношению к рублю."""
    api_key = os.getenv('API_KEY')
    url = f'https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols={currency}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['rates'].get(currency, 1)


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = transaction.get('amount', 0)
    currency = transaction.get('currency')

    if currency == 'USD':
        exchange_rate = get_exchange_rate('USD')
        return amount * exchange_rate
    elif currency == 'EUR':
        exchange_rate = get_exchange_rate('EUR')

        return amount * exchange_rate
    return float(amount)
