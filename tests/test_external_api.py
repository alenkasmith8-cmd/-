import unittest.mock
from typing import Any
from typing import Dict

from src.external_api import convert_to_rub


def test_convert_to_rub_usd() -> None:
    transaction: Dict[str, Any] = {"amount": 100, "currency": "USD"}
    with unittest.mock.patch('src.external_api.get_exchange_rate', return_value=75):
        result = convert_to_rub(transaction)
        assert result == 7500.0


def test_convert_to_rub_eur() -> None:
    transaction: Dict[str, Any] = {"amount": 100, "currency": "EUR"}
    with unittest.mock.patch('src.external_api.get_exchange_rate', return_value=85):
        result = convert_to_rub(transaction)
        assert result == 8500.0


def test_convert_to_rub_rub() -> None:
    transaction: Dict[str, Any] = {"amount": 100, "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 100.0
