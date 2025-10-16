import os
from typing import Any
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Получает курс валюты по отношению к рублю."""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY is missing from environment variables.")

    url = (
        f"https://api.apilayer.com/exchangerates_data/latest?base={base_currency}&symbols="
        f"{target_currency}&apikey={api_key}"
    )
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")

    data = response.json()
    return data['rates'].get(target_currency, 1)


def convert_to_rub(transaction: Dict[str, Any], target_currency: str) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = transaction.get('amount', 0.0)
    currency: str = transaction.get('currency') or ''
    if currency is None:
        currency = ''

    if currency != target_currency:
        exchange_rate: float = get_exchange_rate(currency, target_currency)
        return amount * exchange_rate
    return float(amount)
