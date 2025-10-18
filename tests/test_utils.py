from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import load_transactions_from_json


def test_load_transactions_from_json() -> None:
    mock_data = '[{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]'

    with patch('builtins.open', mock_open(read_data=mock_data)):
        transactions = load_transactions_from_json('data/operations.json')
        assert len(transactions) == 2
        assert transactions[0]['amount'] == 100
        assert transactions[0]['currency'] == "USD"

    # Тест есл файл пуст
    with patch('builtins.open', mock_open(read_data='')):
        transactions = load_transactions_from_json('data/operations.json')
        assert transactions == []

    # Тест если файл не существует
    with patch('builtins.open', side_effect=FileNotFoundError):
        transactions = load_transactions_from_json('data/operations.json')
        assert transactions == []
