import pytest
from datetime import datetime
from src.widget import mask_account_card

class TestMaskAccountCard:
    @pytest.mark.parametrize("input_data, expected_output", [
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 1234", "Счет 1234"),
        ("Карта 1234567812345678", "Карта 1234 56** **** 5678"),
        ("Карта 1234", "Карта 1234"),
        ("Счет 123", "Некорректный номер"),
        ("Некорректная строка", "Некорректный номер"),
        ("", "Некорректный номер"),
    ])
    def test_mask_account_card(self, input_data, expected_output):
        assert mask_account_card(input_data) == expected_output

    @pytest.mark.parametrize("input_data", [
        "Счет 12345678901234567890",   # Длинный номер счета
        "Карта 123456781234567",        # Короткий номер карты
        "Счет abcd"                     # Некорректный номер
    ])
    def test_mask_account_card_invalid(self, input_data):
        assert mask_account_card(input_data) == "Некорректный номер"

# Пример функции get_date (предположим, у вас есть такая функция)
def get_date(date_string: str) -> str:
    try:
        # Предположим, что формат даты всегда в ISO формате
        date_object = datetime.fromisoformat(date_string)
        return date_object.strftime("%d-%m-%Y")
    except ValueError:
        return "Некорректная дата"

class TestGetDate:
    @pytest.mark.parametrize("date_input, expected_output", [
        ("2023-01-01", "01-01-2023"),
        ("2022-12-31", "31-12-2022"),
        ("", "Некорректная дата"),
        ("not-a-date", "Некорректная дата"),
        ("2023-02-30", "Некорректная дата"),  # Неверная дата
    ])
    def test_get_date(self, date_input, expected_output):
        assert get_date(date_input) == expected_output