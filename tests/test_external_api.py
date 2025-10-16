from typing import Any
from typing import Dict
from unittest.mock import patch

from src.external_api import get_exchange_rate


def test_get_exchange_rate() -> None:
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85}}
        rate: float = get_exchange_rate("USD", "EUR")
        assert rate == 0.85


def convert_to_currency(transaction: Dict[str, Any], target_currency: str) -> float:
    """Конвертирует сумму транзакции в указанную валюту."""
    amount: float = transaction.get('amount', 0.0)
    currency: str = transaction.get('currency', 'USD')

    # Если валюта не совпадает с целевой валютой, получаем курс обмена
    if currency != target_currency:
        exchange_rate: float = get_exchange_rate(currency, target_currency)
        return amount * exchange_rate
    return amount  # Если валюта совпадает, возвращаем сумму без изменений
