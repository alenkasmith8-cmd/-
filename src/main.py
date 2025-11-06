import json
import logging
import os
import re
from datetime import datetime

import pandas as pd

import config

# from src.transaction_cvs_xlsx import filter_transactions
# from src.utils import load_transactions
from config import LOG_DIR

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(), logging.FileHandler(os.path.join(LOG_DIR, "app.log"), encoding="utf-8")],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def count_operations_by_category(transactions, categories):
    """
    Подсчитывает общую сумму операций по заданным категориям.

    Args:
        transactions (list): Список транзакций, где каждая транзакция содержит 'amount' и 'category'.
        categories (list): Список категорий для подсчета.

    Returns:
        dict: Словарь, где ключи - категории, а значения - сумма транзакций в этих категориях.
    """
    category_totals = {category: 0 for category in categories}  # Инициализируем словарь с нулевыми значениями

    for transaction in transactions:
        category = transaction.get('category')
        amount = float(transaction.get('operationAmount', {}).get('amount', 0))  # Приводим к float для операций

        if category in categories:  # Проверяем, если категория в заданном списке
            category_totals[category] += amount  # Увеличиваем сумму по категории

    return category_totals


# Функция загрузки транзакций из файла
def load_transactions(file_path: str):
    if file_path.endswith(".json"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                transactions = json.load(file)
                return transactions
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
            raise
    elif file_path.endswith(".csv"):
        try:
            df = pd.read_csv(file_path, sep=";")
            transactions = []
            for _, row in df.iterrows():
                transaction = {
                    "id": str(row["id"]),  # Преобразуем id в строку
                    "state": row["state"],
                    "date": row["date"],
                    "operationAmount": {
                        "amount": row["amount"],
                        "currency": {"name": row["currency_name"], "code": row["currency_code"]},
                    },
                    "from": row["from"],
                    "to": row["to"],
                    "description": row["description"],
                }
                transactions.append(transaction)
            return transactions
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла CSV {file_path}: {e}")
            raise
    elif file_path.endswith(".xlsx"):
        try:
            df = pd.read_excel(file_path)
            transactions = []
            for _, row in df.iterrows():
                transaction = {
                    "id": row["id"],
                    "state": row["state"],
                    "date": row["date"],
                    "operationAmount": {
                        "amount": row["amount"],
                        "currency": {"name": row["currency_name"], "code": row["currency_code"]},
                    },
                    "from": row["from"],
                    "to": row["to"],
                    "description": row["description"],
                }
                transactions.append(transaction)
            return transactions
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла Excel {file_path}: {e}")
            raise
    else:
        logger.error(f"Неподдерживаемый формат файла: {file_path}")
        raise ValueError("Unsupported file format")


# Функция для формата вывода информации о транзакциях
def format_transaction(transaction):
    # Получаем дату и описание
    date = transaction.get("date", "Не указано")
    description = transaction.get("description", "Не указано")

    # Получаем сумму и валюту
    amount = transaction.get("operationAmount", {}).get("amount", "Не указано")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "Не указано")

    # Получаем информацию о счете откуда и куда
    from_account = transaction.get("from", "Не указано")
    to_account = transaction.get("to", "Не указано")

    # Форматируем вывод
    output = f"{date} {description}\n"
    output += f"{from_account} -> {to_account}\n"
    output += f"Сумма: {amount} {currency}\n"
    return output


def filter_transactions(transactions, search_string):
    """Фильтрует список транзакций по строке в описании."""
    # Если строка поиска пустая, возвращаем все транзакции
    if not search_string:
        return transactions

    # Создаем регулярное выражение для поиска с учетом регистра
    search_pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    filtered = []

    for transaction in transactions:
        description = transaction["description"]
        print(f"Checking description: {description}")  # Отладочное сообщение
        # Проверяем наличие паттерна в описании
        if search_pattern.search(description):
            filtered.append(transaction)

    return filtered


def mask_account(account_number: str) -> str:
    """Маскирует номер счета, оставляя только последние 4 цифры."""
    parts = account_number.split()

    # Проверяем, что часть с номером счета есть и что это все цифры
    if len(parts) > 1 and parts[-1].isdigit():
        # Длина счета 6 цифр
        if len(parts[-1]) == 6:
            return f"{parts[0]} **{parts[-1][-3:]}"  # Маскируем все кроме последних 3 цифр
        # Длина счета более 4 цифр
        elif len(parts[-1]) >= 4:
            return f"{parts[0]} **{parts[-1][-4:]}"  # Маскируем все кроме последних 4 цифр

    return account_number  # Возвращаем оригинал, если формат не соответствует


def mask_card(card_info):
    """Маскирует номер карты, оставляя название карты и последние 4 цифры."""
    # Проверяем, если в строке есть название карты (например, "Visa Gold")
    if " " in card_info and not card_info.replace(" ", "").isdigit():
        parts = card_info.rsplit(" ", 1)  # Разделяем название карты и номер
        if len(parts) != 2:
            return card_info  # Если формат некорректный, возвращаем как есть
        card_name = parts[0]  # Название карты
        card_number = parts[1]  # Номер карты
    else:
        card_name = ""  # Название карты отсутствует
        card_number = card_info.strip()  # Убираем лишние пробелы

    # Убираем пробелы из номера карты для обработки
    card_number_clean = card_number.replace(" ", "")

    # Проверяем, что номер карты состоит из цифр и имеет достаточную длину
    if not card_number_clean.isdigit() or len(card_number_clean) < 12:
        return card_info  # Если формат некорректный, возвращаем оригинал

    # Формируем маскированный номер карты
    masked_number = f"{card_number_clean[:4]} {card_number_clean[4:6]}** **** {card_number_clean[-4:]}"

    # Возвращаем название карты и маскированный номер
    if card_name:
        return f"{card_name} {masked_number}"
    return masked_number


def format_date(date_string):
    """Преобразует дату из формата ISO в формат DD.MM.YYYY."""
    try:
        date_obj = datetime.fromisoformat(date_string)
    except ValueError:
        return date_string
    return date_obj.strftime("%d.%m.%Y")


def print_transaction(transaction):
    """Выводит информацию о транзакции в требуемом формате."""
    date = format_date(transaction["date"])
    description = transaction["description"]

    # Получаем значения from и to, обрабатываем пустые значения
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    # Заменяем NaN или пустую строку на пробел
    if isinstance(from_account, float) or not from_account:
        from_account = " "  # Заменить NaN или пустую строку на пробел
    if isinstance(to_account, float) or not to_account:
        to_account = " "  # Заменить NaN или пустую строку на пробел

    # Маскировка
    if "карта" in description.lower():  # Если это перевод с карты на карту
        from_account = mask_card(from_account) if from_account != " " else from_account
        to_account = mask_card(to_account) if to_account != " " else to_account
    else:
        from_account = mask_account(from_account) if "счет" in str(from_account).lower() else mask_card(from_account)
        to_account = mask_account(to_account) if "счет" in str(to_account).lower() else mask_card(to_account)

    # Форматируем вывод в зависимости от типа операции
    if "перевод" in description.lower():
        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
    elif "открытие вклада" in description.lower():
        print(f"{date} {description}")
        print(f"{to_account}")  # Выводим только to_account
    else:
        print(f"{date} {description}")
        print(f"{from_account}")

    # Проверка на наличие ключа 'operationAmount'
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["code"]
        print(f"Сумма: {amount} {currency}\n")
    else:
        print("Сумма: \n")  # информация отсутствует


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        file_path = os.path.join(config.DATA_DIR, "operations.json")  # Используем DATA_DIR
        transactions = load_transactions(file_path)
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_path = os.path.join(config.DATA_DIR, "transactions.csv")  # Используем DATA_DIR
        transactions = load_transactions(file_path)
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_path = os.path.join(config.DATA_DIR, "transactions_excel.xlsx")  # Используем DATA_DIR
        transactions = load_transactions(file_path)
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор.")
        return

    # Фильтрация по статусу
    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию. "
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
            )
            .strip()
            .upper()
        )
        if status in statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            filtered_transactions = [
                t for t in transactions if str(t.get("state", "")).upper() == status
            ]  # Преобразование в строку
            break
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')

    # Дополнительные фильтры
    sort_choice = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_choice == "да":
        order_choice = input("Сортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        if order_choice == "по возрастанию":
            filtered_transactions.sort(key=lambda x: x["date"])
        elif order_choice == "по убыванию":
            filtered_transactions.sort(key=lambda x: x["date"], reverse=True)

    currency_choice = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if currency_choice == "да":
        filtered_transactions = [
            t
            for t in filtered_transactions
            if "operationAmount" in t and t["operationAmount"]["currency"]["code"] == "RUB"
        ]

    description_filter = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if description_filter == "да":
        search_string = input("Введите строку для поиска в описании: ")
        filtered_transactions = filter_transactions(filtered_transactions, search_string)

    # Вывод результатов
    print("Распечатываю итоговый список транзакций...")
    if filtered_transactions:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            print_transaction(transaction)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()
