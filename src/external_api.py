import os

import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла


def convert_amount_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли.
    Args:
        transaction (dict): Словарь с данными о транзакции, содержащий
                            'amount' и 'currency'.

    Returns:
        float: Сумма транзакции в рублях."""

    amount = transaction['operationAmount']['amount']
    currency = transaction['operationAmount']['currency']['code']

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

    if response.status_code == 200:  # Если запрос успешен
        return float(response.json()['result'])  # Возвращаем результат конвертации
    else:
        return float(amount)  # Если API не сработал, возвращаем сумму без изменений
