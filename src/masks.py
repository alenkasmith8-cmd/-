import logging
import os

# Создаем директорию для логов
os.makedirs('logs', exist_ok=True)

# Создаем объект логгера
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

# Настроим обработчик для записи логов в файл
file_handler = logging.FileHandler('logs/masks.log')
file_handler.setLevel(logging.DEBUG)

# Определяем формат логирования
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Отображает первые 6 цифр и последние 4 цифры, остальные символы маскирует звездочками"""
    logger.debug(f'Obtaining masked card number from input: {card_number}')
    card_number = ''.join(filter(str.isdigit, card_number))

    if len(card_number) != 16:
        logger.error("Номер карты должен содержать 16 цифр.")
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.info(f'Masked card number generated: {masked_card_number}')
    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета, оставляя только последние 4 цифры"""
    logger.debug(f'Obtaining masked account number from input: {account_number}')
    account_number = ''.join(filter(str.isdigit, account_number))

    if len(account_number) < 4:
        logger.error("Номер счета должен содержать как минимум 4 цифры.")
        raise ValueError("Номер счета должен содержать как минимум 4 цифры.")

    masked_account_number = f"**{account_number[-4:]}"
    logger.info(f'Masked account number generated: {masked_account_number}')

    return masked_account_number
