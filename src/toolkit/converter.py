from toolkit.constants import (
    ABSOLUTE_ZERO_C,
    ALL_UNITS,
    LENGTH_COEFFS,
    TEMP_FROM_C,
    TEMP_TO_C,
    TEMP_UNITS,
    TEMPERATURE_TOLERANCE,
    WEIGHT_COEFFS,
)
from toolkit.errors import ConverterError


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Переводит температуру из одной единицы измерения в другую"""
    value_c = value * TEMP_TO_C[from_unit][0] + TEMP_TO_C[from_unit][1]
    if value_c < ABSOLUTE_ZERO_C - TEMPERATURE_TOLERANCE:
        raise ConverterError(f"Температура {value} {from_unit} ниже абсолютного нуля")
    if abs(value_c - ABSOLUTE_ZERO_C) <= TEMPERATURE_TOLERANCE:
        value_c = ABSOLUTE_ZERO_C
    temp_result = value_c * TEMP_FROM_C[to_unit][0] + TEMP_FROM_C[to_unit][1]
    return temp_result


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Конвертирует значение"""
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()
    if from_unit not in ALL_UNITS:
        raise ConverterError(f"Неизвестная единица: {from_unit}")
    if to_unit not in ALL_UNITS:
        raise ConverterError(f"Неизвестная единица: {to_unit}")
    if from_unit in LENGTH_COEFFS and to_unit in LENGTH_COEFFS:
        value_m = value * LENGTH_COEFFS[from_unit]
        len_result = value_m / LENGTH_COEFFS[to_unit]
        return len_result
    if from_unit in WEIGHT_COEFFS and to_unit in WEIGHT_COEFFS:
        value_kg = value * WEIGHT_COEFFS[from_unit]
        wei_result = value_kg / WEIGHT_COEFFS[to_unit]
        return wei_result
    if from_unit in TEMP_UNITS and to_unit in TEMP_UNITS:
        return convert_temperature(value, from_unit, to_unit)
    raise ConverterError(f"Нельзя перевести {from_unit} в {to_unit}")
