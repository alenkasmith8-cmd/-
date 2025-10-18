from unittest.mock import patch
from src.external_api import convert_amount_to_rub


@patch('requests.get')
def test_convert_amount_to_rub(mock_get) -> None:
    transaction = {"amount": 100, "currency": "USD"}

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 7500.0}

    # Перед тестированием проверьте, что установили ключ API
    with patch.dict('os.environ', {'API_KEY': 'fake_api_key'}):
        amount_in_rub = convert_amount_to_rub(transaction)
        assert amount_in_rub == 7500.0

    # тестирование уже в рублях
    transaction_rub = {"amount": 100, "currency": "RUB"}
    assert convert_amount_to_rub(transaction_rub) == 100.0
