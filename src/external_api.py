import os
from typing import Any
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Получает курс валюты"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY is missing from environment variables.")

    url = f"https://api.apilayer.com/currency_data/convert?from={base_currency}&to={target_currency}&amount=1"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")

    data = response.json()
    return data['result']


def convert_to_currency(transaction: Dict[str, Any], target_currency: str) -> float:
    """Конвертирует сумму транзакции в указанную валюту."""
    amount: float = transaction.get('amount', 0.0)
    currency: str = transaction.get('currency', 'USD')

    # Если валюта не совпадает с целевой, получаем курс обмена
    if currency != target_currency:
        exchange_rate: float = get_exchange_rate(currency, target_currency)
        return amount * exchange_rate
    return amount  # Если валюта совпадает, возвращаем сумму без изменений
