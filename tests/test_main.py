import csv
import json
import logging
import os
import re
from pathlib import Path

import pytest

import src.main
from config import LOG_DIR

base_dir = Path(__file__).parent
json_file_path = "data/operations.json"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(), logging.FileHandler(os.path.join(LOG_DIR, "app.log"), encoding="utf-8")],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# Пример использования
# json_file = os.path.join(DATA_DIR, 'operations.json')
# csv_file = os.path.join(DATA_DIR, 'transactions.csv')
# excel_file = os.path.join(DATA_DIR, 'transactions_excel.xlsx')


def test_count_operations_by_category():
    transactions = [
        {"operationAmount": {"amount": "1000"}, "category": "Зарплата"},
        {"operationAmount": {"amount": "500"}, "category": "Зарплата"},
        {"operationAmount": {"amount": "200"}, "category": "Покупка"},
        {"operationAmount": {"amount": "300"}, "category": "Покупка"},
    ]
    categories = ["Зарплата", "Покупка"]

    result = src.main.count_operations_by_category(transactions, categories)

    assert result["Зарплата"] == 1500  # Сумма зарплаты
    assert result["Покупка"] == 500  # Сумма покупок

    # Тест с категориями, отсутствующими в транзакциях
    categories = ["Зарплата", "Покупка", "Неправильная категория"]
    result = src.main.count_operations_by_category(transactions, categories)

    assert result["Неправильная категория"] == 0  # Проверяем, что отсутствующая категория равна 0


def test_load_transactions_json_success(tmp_path):
    # Создаем временный JSON-файл
    data = [{"id": 1, "state": "EXECUTED", "date": "2023-01-01"}]
    file = tmp_path / "test.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    transactions = src.main.load_transactions(str(file))
    assert transactions == data


def test_load_transactions_json_error(tmp_path):
    # Создаем поврежденный JSON-файл
    file = tmp_path / "test.json"
    file.write_text("{invalid_json}", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        src.main.load_transactions(str(file))


def test_load_transactions_csv_success(tmp_path):
    # Создаем временный CSV-файл
    content = (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "1;EXECUTED;2023-01-01;100;USD;1234;5678;Test"
    )
    file = tmp_path / "test.csv"
    file.write_text(content, encoding="utf-8")

    transactions = src.main.load_transactions(str(file))
    assert len(transactions) == 1
    assert transactions[0]["id"] == "1"


def test_load_transactions_unsupported_format(tmp_path):
    # Создаем файл с неподдерживаемым форматом
    file = tmp_path / "test.txt"
    file.write_text("Hello world", encoding="utf-8")

    with pytest.raises(ValueError):
        src.main.load_transactions(str(file))


def test_load_transactions_invalid_format():  # ТЕСТЫ ПРОВЕРЕННЫЕ
    with pytest.raises(ValueError, match="Unsupported file format"):  # %
        src.main.load_transactions("test_data.txt")


def test_load_transactions_json(setup_files):
    test_json_file, _ = setup_files
    with open(test_json_file, "r", encoding="utf-8") as f:
        print(f.read())  # Вывод содержимого JSON файла
    transactions = src.main.load_transactions(test_json_file)
    assert len(transactions) == 1
    assert transactions[0]["id"] == "1"
    assert transactions[0]["operationAmount"]["amount"] == "1000"
    assert transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_load_transactions_csv(setup_files):
    _, test_csv_file = setup_files
    with open(test_csv_file, "r", encoding="utf-8") as f:
        print(f.read())  # Вывод содержимого CSV файла
    transactions = load_transactions_(test_csv_file)
    assert len(transactions) == 1
    assert transactions[0]["id"] == "1"  # Теперь это строка
    assert transactions[0]["operationAmount"]["amount"] == "1000"
    assert transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def load_transactions_(file_path):
    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif file_path.endswith(".csv"):
        transactions = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")

            # Проверяем, что заголовки загружены
            if reader.fieldnames is None:
                raise ValueError("CSV file does not have headers")
            # Очищаем заголовки от лишних пробелов
            headers = [header.strip() for header in reader.fieldnames]
            for row in reader:
                # row должен быть словарем
                if not isinstance(row, dict):
                    raise ValueError("Row is not a dictionary")

                # Используем метод get для безопасного доступа к значениям
                transaction = {
                    "id": str(row.get("id", "")),  # Преобразуем id в строку
                    "state": row.get("state", ""),
                    "date": row.get("date", ""),
                    "operationAmount": {
                        "amount": row.get("amount", ""),
                        "currency": {"name": row.get("currency_name", ""), "code": row.get("currency_code", "")},
                    },
                    "from": row.get("from", ""),
                    "to": row.get("to", ""),
                    "description": row.get("description", ""),
                }
                transactions.append(transaction)

        return transactions
    else:
        raise ValueError("Unsupported file format")


def filter_transactions_(transactions, keyword):  # название функции изменил '_'
    keyword = keyword.lower()  # Приводим ключевое слово к нижнему регистру
    return [tx for tx in transactions if keyword in tx["description"].lower()]


@pytest.fixture(scope="module")
def setup_files():
    test_json_file = "test_data.json"
    test_csv_file = "test_data.csv"

    # JSON тестовые данные
    with open(test_json_file, "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "id": "1",
                    "state": "EXECUTED",
                    "date": "2023-11-10T10:00:00Z",
                    "operationAmount": {"amount": "1000", "currency": {"name": "рубль", "code": "RUB"}},
                    "from": "Счет 1234567890123456",
                    "to": "Счет 6543210987654321",
                    "description": "Перевод с карты на карту",
                }
            ],
            f,
        )

    # CSV тестовые данные
    with open(test_csv_file, "w", encoding="utf-8") as f:
        f.write("id;state;date;amount;currency_name;currency_code;from;to;description\n")
        f.write(
            "1;EXECUTED;2023-11-10T10:00:00Z;1000;рубль;RUB;Счет 1234567890123456;"
            "Счет 6543210987654321;Перевод с карты на карту\n"
        )

    yield test_json_file, test_csv_file

    os.remove(test_json_file)
    os.remove(test_csv_file)


def test_load_transactions_json_(setup_files):  # название функции изменил '_'
    test_json_file, _ = setup_files
    transactions = src.main.load_transactions(test_json_file)
    assert len(transactions) == 1
    assert transactions[0]["id"] == "1"
    assert transactions[0]["operationAmount"]["amount"] == "1000"
    assert transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def filter_transactions_filter(transactions, keyword):
    # Создаем регулярное выражение для поиска "карта" и всех ее форм
    pattern = re.compile(r"\b" + re.escape(keyword[:-1]) + r"\w\b", re.IGNORECASE)

    print(f"Keyword pattern: '{pattern.pattern}'")  # Печатаем паттерн для поиска
    filtered_transactions = []

    for tx in transactions:
        description_cleaned = tx["description"].strip().lower()  # Очищаем строку
        print(f"Original description: '{tx['description']}'")  # Печатаем оригинальное описание
        print(f"Cleaned description: '{description_cleaned}'")  # Печатаем очищенное описание

        # Проверяем наличие ключевого слова с помощью регулярного выражения
        if pattern.search(description_cleaned):
            filtered_transactions.append(tx)

    print(f"Filtered transactions: {filtered_transactions}")  # Печатаем отфильтрованные транзакции
    return filtered_transactions


def test_filter_transactions_empty_keyword():
    transactions = [{"description": "Перевод с карты на карту"}, {"description": "Перевод организации"}]
    filtered = src.main.filter_transactions(transactions, "")
    assert len(filtered) == 2  # Все транзакции должны быть возвращены


def test_filter_transactions_case_insensitivity():
    transactions = [
        {"description": "Перевод с КАРТЫ на карту"},  # %
        {"description": "Перевод организации"},
        {"description": "перевод с карты на карту"},
    ]
    filtered_a = src.main.filter_transactions(transactions, "карт")
    assert len(filtered_a) == 2  # Должно найти оба варианта


def test_filter_transactions_no_matches():
    transactions = [{"description": "Перевод организации"}, {"description": "Перевод с карты на счет"}]  # %
    filtered = src.main.filter_transactions(transactions, "некорректное слово")
    assert len(filtered) == 0


def test_mask_account():
    masked = src.main.mask_account("Счет 1234567890123456")
    assert masked == "Счет **3456"


def test_mask_card():
    masked = src.main.mask_card("1234567890123456")
    assert masked == "1234 56** **** 3456"


def test_format_date():
    formatted = src.main.format_date("2023-11-10T10:00:00Z")
    assert formatted == "10.11.2023"


def test_mask_account_invalid_input():
    masked = src.main.mask_account("Некорректный ввод")  # %
    assert masked == "Некорректный ввод"  # Если формат не соответствует, то возвращаем оригинал


def test_mask_card_invalid_input():
    masked = src.main.mask_card("Некорректный ввод")  # %
    assert masked == "Некорректный ввод"  # Если формат не соответствует, то возвращаем оригинал


def test_format_date_invalid_input():
    formatted = src.main.format_date("Некорректный ввод")  # %
    assert formatted == "Некорректный ввод"  # Если формат не соответствует, то возвращаем оригинал


def test_load_transactions_empty_file():
    empty_file_path = "empty_file.json"
    with open(empty_file_path, "w", encoding="utf-8") as f:
        f.write("")  # Создаем пустой файл

    with pytest.raises(json.JSONDecodeError):
        src.main.load_transactions(empty_file_path)


def test_filter_transactions_partial_match():
    transactions = [
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод с карточки на счет"},
        {"description": "Перевод организации"},
    ]
    filtered = src.main.filter_transactions(transactions, "кар")
    assert len(filtered) == 2  # Должно найти оба варианта


def test_mask_account_various_formats():
    assert src.main.mask_account("Счет 1234 5678 9012 3456") == "Счет **3456"
    assert src.main.mask_account("Счет 123456") == "Счет **456"
    assert src.main.mask_account("Некорректный ввод") == "Некорректный ввод"
    assert src.main.mask_account("Счет 1234 5678 9012 3456") == "Счет **3456"
    assert src.main.mask_account("Счет 123456") == "Счет **456"
    assert src.main.mask_account("Счет 123") == "Счет 123"  # Если менее 4 цифр, возвращаем оригинал
    assert src.main.mask_account("Счет нечисловое") == "Счет нечисловое"  # Тест на нечисловые значения


def test_mask_card_various_formats():
    assert src.main.mask_card("1234 5678 9012 3456") == "1234 56** **** 3456"
    assert src.main.mask_card("1234567890123456") == "1234 56** **** 3456"
    assert src.main.mask_card("Некорректный ввод") == "Некорректный ввод"


def test_format_date_various_formats():
    assert src.main.format_date("2023-11-10T10:00:00Z") == "10.11.2023"
    assert src.main.format_date("2023-11-10") == "10.11.2023"  # Предполагаем, что функция поддерживает другой формат
    assert src.main.format_date("Некорректный ввод") == "Некорректный ввод"  # Ожидаем оригинал


def test_print_transaction_various_formats(capsys):
    transaction = {
        "description": "Перевод с карты на карту",
        "operationAmount": {"amount": 1000, "currency": {"code": "RUB"}},
        "date": "2023-01-01",
    }

    src.main.print_transaction(transaction)
    captured = capsys.readouterr()

    assert "Перевод с карты на карту" in captured.out
    assert "1000" in captured.out  # Проверяем, что вывод содержит сумму


# Тесты для функции format_transaction
def test_format_transaction():
    # Тест 1: Полные данные
    transaction = {
        "date": "2023-10-01",
        "description": "Перевод средств",
        "operationAmount": {"amount": "1000", "currency": {"name": "RUB"}},
        "from": "Счет 1234",
        "to": "Счет 5678",
    }
    expected_output = "2023-10-01 Перевод средств\nСчет 1234 -> Счет 5678\nСумма: 1000 RUB\n"
    assert src.main.format_transaction(transaction) == expected_output

    # Тест 2: Отсутствие некоторых данных
    transaction = {
        "date": "2023-10-02",
        "description": "Оплата",
        "operationAmount": {"amount": "500", "currency": {}},
        "from": "Счет 1234",
        "to": "Не указано",
    }
    expected_output = "2023-10-02 Оплата\nСчет 1234 -> Не указано\nСумма: 500 Не указано\n"
    assert src.main.format_transaction(transaction) == expected_output

    # Тест 3: Отсутствие всех данных
    transaction = {}
    expected_output = "Не указано Не указано\nНе указано -> Не указано\nСумма: Не указано Не указано\n"
    assert src.main.format_transaction(transaction) == expected_output

    # Тест 4: Отсутствие даты и описания
    transaction = {
        "operationAmount": {"amount": "200", "currency": {"name": "USD"}},
        "from": "Счет 1111",
        "to": "Счет 2222",
    }
    expected_output = "Не указано Не указано\nСчет 1111 -> Счет 2222\nСумма: 200 USD\n"
    assert src.main.format_transaction(transaction) == expected_output

    # Тест 5: Проверка на наличие пробелов
    transaction = {
        "date": "2023-10-03",
        "description": "   Перевод   ",
        "operationAmount": {"amount": "300", "currency": {"name": "EUR"}},
        "from": "Счет 3333",
        "to": "Счет 4444",
    }
    expected_output = "2023-10-03    Перевод   \nСчет 3333 -> Счет 4444\nСумма: 300 EUR\n"
    assert src.main.format_transaction(transaction) == expected_output


@pytest.mark.timeout(10)
def test_main_json(monkeypatch, tmp_path):
    # Создаем временный JSON-файл
    data = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01",
            "description": "Тестовая транзакция",
            "operationAmount": {"amount": "1000", "currency": {"name": "Ruble", "code": "RUB"}},
        }
    ]
    # Создаем файл с использованием tmp_path
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    # Эмулируем ввод пользователя
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: {
            "Пользователь: ": "1",  # Выбор первого пункта меню
            "Введите статус, по которому необходимо выполнить фильтрацию."
            " Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: ": "EXECUTED",
            "Отсортировать операции по дате? Да/Нет\nПользователь: ": "нет",  # Ответ на сортировку
            "Выводить только рублевые транзакции? Да/Нет\nПользователь: ": "да",  # Ответ на выбор валюты
            "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
            "Пользователь: ": "нет",  # Ответ на фильтрацию по описанию
        }[prompt],
    )  # Эмулируем ввод для каждого ожидаемого запроса

    # Установите DATA_DIR для теста
    monkeypatch.setattr("config.DATA_DIR", str(tmp_path))  # Устанавливаем временный путь

    # Вызов функции main
    print("Before calling main()")
    src.main.main()
    print("After calling main()")


if __name__ == "__main__":
    pytest.main()
