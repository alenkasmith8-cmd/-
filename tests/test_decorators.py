import pytest

from src.decorators import log


@log()
def successful_function(x: int, y: int) -> int:
    return int(x + y)  # Явное приведение к int для устранения ошибки


@log()
def error_function(x: int) -> float:  # Измените тип возвращаемого значения на float
    return 1 / x  # Деление на ноль вызовет исключение


def test_successful_function(capsys: pytest.CaptureFixture) -> None:
    result: int = successful_function(3, 4)

    assert result == 7
    assert "Запуск функции: successful_function in captured.out"
    assert "Функция: successful_function завершена успешно, результат: 7 in captured.out"


def test_error_function(capsys: pytest.CaptureFixture) -> None:
    # Проверяем, что функция вызовет ошибку
    with pytest.raises(ZeroDivisionError):
        error_function(0)

    assert "Запуск функции: error_function in captured.out"
    assert "Функция: error_function завершена с ошибкой: ZeroDivisionError in captured.out"
