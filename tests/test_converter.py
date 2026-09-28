import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError


def test_mm_m() -> None:
    assert convert(1000, "mm", "m") == 1

def test_kg_g() -> None:
    assert convert(1.5, "kg", "g") == 1500

def test_c_f() -> None:
    assert convert(0, "c", "f") == 32

def test_abs_zero() -> None:
    assert convert(-273.15, "c", "k") == 0

def test_below_zero() -> None:
    with pytest.raises(ConverterError):
        convert(-300, "c", "f")

def test_incompatible_units() -> None:
    with pytest.raises(ConverterError):
        convert(100, "kg", "m")

def test_upper_case() -> None:
    assert convert(10, "Cm", "MM") == 100

def test_unknown_unit() -> None:
    with pytest.raises(ConverterError):
        convert(10, "abc", "m")
