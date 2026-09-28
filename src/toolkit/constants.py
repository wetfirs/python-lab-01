ALL_UNITS = ["mm", "cm", "m", "km", "g", "kg", "c", "f", "k"]

LENGTH_COEFFS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
}

WEIGHT_COEFFS = {
    "g": 0.001,
    "kg": 1,
}

TEMP_UNITS = {"c", "f", "k"}

TEMP_TO_C = {
    "c": (1, 0),
    "k": (1, -273.15),
    "f": (5 / 9, -32 * 5 / 9),
}

TEMP_FROM_C = {
    "c": (1, 0),
    "k": (1, 273.15),
    "f": (9 / 5, 32),
}

ABSOLUTE_ZERO_C = -273.15

TEMPERATURE_TOLERANCE = 1e-9
