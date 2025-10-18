import os
from typing import Dict
import requests


def convert_amount_to_rub(transaction: Dict[str, float]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    # Если валюта уже в рублях, возвращаем сумму без изменений
    if currency == 'RUB':
        return float(amount)

    # Получаем курс обмена из API
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY is missing from environment variables.")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")

    data = response.json()
    return float(data.get('result', 0.0))  # Возвращаем значение, возвращенное API
