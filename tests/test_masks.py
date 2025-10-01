import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


class TestGetMaskCardNumber:
    def test_valid_card_number(self) -> None:
        assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

    def test_valid_card_number_with_spaces(self) -> None:
        assert get_mask_card_number(" 7000 7922 8960 6361 ") == "7000 79** **** 6361"

    def test_incorrect_card_number_length(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("70007922")
        assert str(excinfo.value) == "Номер карты должен содержать 16 цифр."

    def test_no_card_number(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("")
        assert str(excinfo.value) == "Номер карты должен содержать 16 цифр."


class TestGetMaskAccount:
    def test_valid_account_number(self) -> None:
        assert get_mask_account("73654108430135874305") == "**4305"

    def test_valid_account_number_with_spaces(self) -> None:
        assert get_mask_account(" 7365 4108 4301 3587 ") == "**3587"

    def test_incorrect_account_number_length(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("123")
        assert str(excinfo.value) == "Номер счета должен содержать как минимум 4 цифры."

    def test_no_account_number(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("Счет")
        assert str(excinfo.value) == "Номер счета должен содержать как минимум 4 цифры."


if __name__ != "__main__":
    pass
else:
    pytest.main()
