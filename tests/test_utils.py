from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import read_json_file


def test_read_json_file() -> None:
    # Подготовка имитации открытия файла
    mock_data = '{"transactions": [{"amount": 100, "currency": "USD"}]}'
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = read_json_file('data/operations.json')
        assert result == [{"amount": 100, "currency": "USD"}]


def test_read_json_file_empty() -> None:
    # Проверяем что возвращается пустой список для пустого файла
    with patch('builtins.open', mock_open(read_data='')):
        result = read_json_file('data/empty.json')
        assert result == []


def test_read_json_file_not_exist() -> None:
    # Проверяем что возвращается пустой список если файл не существует

    result = read_json_file('data/non_existent.json')
    assert result == []
