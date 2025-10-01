import unittest
from typing import Any
from typing import Dict
from typing import List

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


class TestGenerators(unittest.TestCase):

    def setUp(self) -> None:
        self.transactions: List[Dict[str, Any]] = [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {"name": "руб.", "code": "RUB"},
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160",
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229",
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {"name": "руб.", "code": "RUB"},
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657",
            },
        ]

    # Тестирование функции filter_by_currency
    def test_filter_by_currency_valid(self) -> None:
        """Проверяем, что функция корректно фильтрует транзакции по заданной валюте."""
        usd_transactions = list(filter_by_currency(self.transactions, "USD"))
        self.assertEqual(len(usd_transactions), 3)

    def test_filter_by_currency_no_transactions(self) -> None:
        """Проверяем, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют."""
        rub_transactions = list(filter_by_currency(self.transactions, "EUR"))
        self.assertEqual(len(rub_transactions), 0)

    def test_filter_by_currency_empty_list(self) -> None:
        """Убедимся, что генератор корректно обрабатывает пустой список."""
        empty_transactions: List[Dict[str, Any]] = []
        result = list(filter_by_currency(empty_transactions, "USD"))
        self.assertEqual(result, [])

    def test_filter_by_currency_no_matching_currency(self) -> None:
        """Убедимся, что генератор не завершает ошибкой при обработке списка без валютных операций."""
        no_match_transactions: List[Dict[str, Any]] = [{"operationAmount": {"currency": {"code": "EUR"}}}]
        result = list(filter_by_currency(no_match_transactions, "USD"))
        self.assertEqual(result, [])

    # Тестирование функции transaction_descriptions
    def test_transaction_descriptions(self) -> None:
        """Проверяем, что функция возвращает корректные описания для каждой транзакции."""
        descriptions = list(transaction_descriptions(self.transactions))
        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        self.assertEqual(descriptions, expected_descriptions)

    def test_transaction_descriptions_empty_list(self) -> None:
        """Тестируем работу функции с пустым списком."""
        empty_transactions: List[Dict[str, Any]] = []
        descriptions = list(transaction_descriptions(empty_transactions))
        self.assertEqual(descriptions, [])

    # Тестирование генератора card_number_generator
    def test_card_number_generator(self) -> None:
        """Проверяем, что генератор выдает правильные номера карт в заданном диапазоне."""
        card_numbers = list(card_number_generator(1, 5))
        expected_numbers = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]
        self.assertEqual(card_numbers, expected_numbers)

    def test_card_number_generator_formatting(self) -> None:
        """Проверяем корректность форматирования номеров карт."""
        card_numbers = list(card_number_generator(10, 10))
        self.assertEqual(card_numbers, ["0000 0000 0000 0010"])

    def test_card_number_generator_extremes(self) -> None:
        """Убедимся, что генератор корректно обрабатывает крайние значения диапазона."""
        card_numbers_start = list(card_number_generator(0, 0))
        card_numbers_end = list(card_number_generator(1000, 1000))
        self.assertEqual(card_numbers_start, ["0000 0000 0000 0000"])
        self.assertEqual(card_numbers_end, ["0000 0000 0000 1000"])


if __name__ == "__main__":
    unittest.main()
