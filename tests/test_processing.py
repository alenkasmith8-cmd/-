from typing import Dict
from typing import List

import pytest

from src.processing import filter_by_state
from src.processing import sort_by_date


@pytest.fixture
def sample_data() -> List[Dict[str, str]]:
    return [
        {"id": "1", "state": "EXECUTED", "date": "2023-01-01"},
        {"id": "2", "state": "PENDING", "date": "2023-01-02"},
        {"id": "3", "state": "EXECUTED", "date": "2023-01-03"},
        {"id": "4", "state": "CANCELED", "date": "2023-01-01"},
    ]


class TestFilterByState:
    def test_filter_executed(self, sample_data: List[Dict[str, str]]) -> None:
        result = filter_by_state(sample_data, state="EXECUTED")
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["id"] == "3"

    def test_filter_no_results(self, sample_data: List[Dict[str, str]]) -> None:
        result = filter_by_state(sample_data, state="UNKNOWN")
        assert result == []

    def test_filter_pending(self, sample_data: List[Dict[str, str]]) -> None:
        result = filter_by_state(sample_data, state="PENDING")
        assert len(result) == 1
        assert result[0]["id"] == "2"


class TestSortByDate:
    def test_sort_by_date_ascending(self, sample_data: List[Dict[str, str]]) -> None:
        result = sort_by_date(sample_data, reverse=False)  # Сортировка по возрастанию
        print("Результат сортировки (по возрастанию):", result)  # Для отладки
        assert result[0]["id"] == "1"  # id = 1 (2023-01-01)
        assert result[1]["id"] == "4"  # id = 4 (тоже 2023-01-01)
        assert result[2]["id"] == "2"  # id = 2 (2023-01-02)
        assert result[3]["id"] == "3"  # id = 3 (2023-01-03)

    def test_sort_by_date_descending(self, sample_data: List[Dict[str, str]]) -> None:
        result = sort_by_date(sample_data, reverse=True)  # Сортировка по убыванию
        print("Результат сортировки (по убыванию):", result)  # Для отладки
        assert result[0]["id"] == "3"  # id = 3 (2023-01-03)
        assert result[1]["id"] == "2"  # id = 2 (2023-01-02)
        assert result[2]["id"] == "4"  # id = 4 (тоже 2023-01-01)
        assert result[3]["id"] == "1"  # id = 1 (тоже 2023-01-01)

    def test_sort_empty_list(self) -> None:
        result = sort_by_date([])
        assert result == []

    def test_sort_with_same_dates(self) -> None:
        data = [
            {"id": "1", "state": "EXECUTED", "date": "2023-01-01"},
            {"id": "2", "state": "PENDING", "date": "2023-01-01"},
        ]
        result = sort_by_date(data)
        # Проверяем порядок
        assert result[0]["id"] == "1"  # id = 1 должен быть первым
        assert result[1]["id"] == "2"  # id = 2 должен быть вторым

    def test_sort_invalid_dates(self) -> None:
        invalid_data = [
            {"id": "1", "state": "EXECUTED", "date": "invalid-date"},
            {"id": "2", "state": "PENDING", "date": "2023-01-02"},
            {"id": "3", "state": "EXECUTED", "date": "2023-01-03"},
        ]
        with pytest.raises(ValueError):
            sort_by_date(invalid_data)
