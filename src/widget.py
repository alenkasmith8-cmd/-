def mask_account_card(account_info: str) -> str:
    """
    Скрывает часть номера счета или карты.
    :param account_info: Строка, содержащая информацию о счете или карте.
    :return: Строка с замаскированным номером счета или сообщение об ошибке.
    """
    account_info = account_info.strip()

    def is_valid_number(number: str) -> bool:
        return number.isdigit() and 4 <= len(number) <= 19

    parts = account_info.split()
    if len(parts) < 2:
        return "Некорректный номер"  # Если не хватает частей для проверки

    number = parts[-1]  # Получаем номер

    if "Счет" in account_info:
        if not is_valid_number(number):
            return "Некорректный номер"

        # Маскировка номера счета
        if len(number) > 4:
            masked_number = '**' + number[-4:]  # Оставляем последние 4 цифры и добавляем 2 звёздочки перед ними
        else:
            masked_number = number  # Если 4 или меньше, оставляем как есть

        return f"Счет {masked_number}"  # Возвращаем итоговую строку

    elif "Карта" in account_info:
        if not is_valid_number(number):
            return "Некорректный номер"

        if len(number) <= 4:
            return f"{' '.join(parts[:-1])} {number}"

        # Маскируем номер карты
        masked_number = number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]
        return f"{' '.join(parts[:-1])} {masked_number}"

    return "Некорректный номер"  # Если ни одно условие не было выполнено
