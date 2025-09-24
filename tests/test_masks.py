import sys
print(sys.path)
import pytest
from masks import get_mask_card_number, get_mask_account

class TestGetMaskCardNumber:
    def test_valid_card_number(self):
        assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

    def test_valid_card_number_with_spaces(self):
        assert get_mask_card_number(" 7000 7922 8960 6361 ") == "7000 79** **** 6361"

    def test_incorrect_card_number_length(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("70007922")
        assert str(excinfo.value) == "Номер карты должен содержать 16 цифр."

    def test_no_card_number(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("")
        assert str(excinfo.value) == "Номер карты должен содержать 16 цифр."


class TestGetMaskAccount:
    def test_valid_account_number(self):
        assert get_mask_account("73654108430135874305") == "**4305"

    def test_valid_account_number_with_spaces(self):
        assert get_mask_account(" 7365 4108 4301 3587 ") == "**3587"

    def test_incorrect_account_number_length(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("123")
        assert str(excinfo.value) == "Номер счета должен содержать как минимум 4 цифры."

    def test_no_account_number(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("Счет")
        assert str(excinfo.value) == "Номер счета должен содержать как минимум 4 цифры."


if __name__ == "__main__":
    pytest.main()