from typing import Text, Any, Optional


def to_lower(possible_string: Any) -> Text:
    "Helper function to transform strings to lower case"
    value = ""
    try:
        value = possible_string.lower()
    except AttributeError:
        pass

    return value


def cast_to_bool(value: Any) -> bool:

    if isinstance(value, str):
        return value.lower() == "true"
    if isinstance(value, (float, int)):
        return bool(value)
    if isinstance(value, bool):
        return value

    return False


def gravity_to_plato(gravity: Optional[float]) -> Optional[float]:
    if gravity is None:
        return None

    return (-463.37) + (668.72 * gravity) - (205.35 * (gravity * gravity))
