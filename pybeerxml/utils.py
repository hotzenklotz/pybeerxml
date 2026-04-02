from typing import Any


def to_lower(possible_string: Any) -> str:
    "Helper function to transform strings to lower case"
    try:
        return possible_string.lower()
    except AttributeError:
        return ""


def cast_to_bool(value: Any) -> bool:
    if isinstance(value, str):
        return value.lower() == "true"
    if isinstance(value, (float, int)):
        return bool(value)
    if isinstance(value, bool):
        return value
    return False


def gravity_to_plato(gravity: float | None) -> float | None:
    if gravity is None:
        return None
    return (-463.37) + (668.72 * gravity) - (205.35 * (gravity * gravity))
