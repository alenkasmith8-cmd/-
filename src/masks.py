def get_mask_card_number(card_number: str) -> str:
    """Отображает первые 6 цифр и последние 4 цифры, остальные символы маскирует звездочками"""
    card_number = ''.join(filter(str.isdigit, card_number))
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета, оставляя только последние 4 цифры"""
    account_number = ''.join(filter(str.isdigit, account_number))
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать как минимум 4 цифры.")

    masked_account_number = f"**{account_number[-4:]}"

    return masked_account_number
