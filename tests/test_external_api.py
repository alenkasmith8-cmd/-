from unittest.mock import patch

from src.external_api import get_exchange_rate


def test_get_exchange_rate() -> None:
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 0.85}
        rate: float = get_exchange_rate("USD", "EUR")
        assert rate == 0.85


def convert_to_currency() -> None:
    """Конвертирует сумму транзакции в указанную валюту."""
    transaction = {"amount": 100, "currency": "USD"}
    target_currency = "EUR"

    with patch('src.external_api.get_exchange_rate') as mock_get_exchange_rate:
        # Допустим, что курс обмена USD на EUR равен 0.85
        mock_get_exchange_rate.return_value = 0.85
        converted_amount = convert_to_currency(transaction, target_currency)

        # Проверяем, что результат соответствует ожиданиям
        assert converted_amount == 85.0
