def mask_account_card(account_info: str) -> str:
    """
    Скрывает часть номера счета.
    :param account_info: Строка, содержащая информацию о счете. Если в строке есть слово "Счет",
    будет скрыта вся часть, кроме последних 4 цифр.
    :return: Строка с замаскированным номером счета или сообщение об ошибке.
    """
    account_info = account_info.strip()

    # Функция для проверки корректности номера
    def is_valid_number(number: str) -> bool:
        return number.isdigit() and 4 <= len(number) <= 19

    if "Счет" in account_info:
        number = account_info.split()[-1]

        # Проверка на корректность номера
        if not is_valid_number(number):
            return "Некорректный номер"

        masked_number = '*' * (len(number) - 4) + number[-4:]
        return f"Счет {masked_number}"
    else:
        number = account_info.split()[-1]

        # Проверка на корректность номера
        if not is_valid_number(number):
            return "Некорректный номер"

        masked_number = number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]
        return f"{' '.join(account_info.split()[:-1])} {masked_number}"