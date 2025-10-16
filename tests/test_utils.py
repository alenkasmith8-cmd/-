from typing import Any
from typing import Dict
from typing import List
from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import read_json_file


# Проверка чтения существующего файла
def test_read_json_file_list() -> None:
    mock_data: str = '[{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]'
    file_path = 'data/transactions.json'

    with patch('builtins.open', mock_open(read_data=mock_data)):
        result: List[Dict[str, Any]] = read_json_file(file_path)
        assert result == [{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]


# Проверка отсутствия файла
def test_read_json_file_not_exist(mock_data=None, file_path=None) -> None:
    result: List[Dict[str, Any]] = read_json_file('data/non_existent.json')
    assert result == []  # Проверяем, что результат - пустой список

    with patch('builtins.open', mock_open(read_data=mock_data)):
        result: List[Dict[str, Any]] = read_json_file(file_path)
        assert result == [{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]


# Проверка отсутствия файла
def test_read_json_file_not_exist() -> None:
    result = read_json_file('data/non_existent.json')
    assert result == []  # Проверяем, что результат - пустой список
