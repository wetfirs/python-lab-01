import pytest

from toolkit.calculator import calculate
from toolkit.errors import CalculatorError


def test_priority() -> None:
    assert calculate("2+3*4") == 14

def test_division() -> None:
    assert calculate("10 / 4") == 2.5

def test_unary_minus() -> None:
    assert calculate("-2 * -3") == 6

def test_plus_minus() -> None:
    assert calculate("1+-2") == -1

def test_empty() -> None:
    with pytest.raises(CalculatorError):
        calculate("")

def test_two_operators() -> None:
    with pytest.raises(CalculatorError):
        calculate("2*/3")

def test_invalid_char() -> None:
    with pytest.raises(CalculatorError):
        calculate("2+a")

def test_div_by_zero() -> None:
    with pytest.raises(CalculatorError):
        calculate("1/0")

def test_brackets() -> None:
    assert calculate("(-1)*(2+5)*10 - 12/(5-7)") == -64

def test_integer_division() -> None:
    assert calculate("20 // 8") == 2

def test_integer_division_negative() -> None:
    assert calculate("-7 // 2") == -4

def test_mod() -> None:
    assert calculate("30 % 7") == 2

def test_mod_negative() -> None:
    assert calculate("7 % -2") == -1

def test_real_numbers() -> None:
    assert calculate("2.5 * 3.2") == 8
