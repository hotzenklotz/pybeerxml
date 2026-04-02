from typing import Any


def to_lower(possible_string: Any) -> str:
    """Return ``possible_string.lower()``, or ``""`` for non-string values.

    Args:
        possible_string: Any value. Non-strings (including ``None``) return ``""``.

    Returns:
        Lower-cased string, or ``""`` if the value has no ``lower`` method.
    """
    try:
        return possible_string.lower()
    except AttributeError:
        return ""


def cast_to_bool(value: Any) -> bool:
    """Coerce a BeerXML field value to a Python ``bool``.

    BeerXML represents boolean values as the strings ``"TRUE"`` / ``"FALSE"``.
    Numeric values follow standard Python truthiness.

    Args:
        value: The raw value to coerce — typically a string, int, float, or bool.

    Returns:
        ``True`` or ``False``.  Unknown types (e.g. ``None``, lists) return ``False``.
    """
    if isinstance(value, str):
        return value.lower() == "true"
    if isinstance(value, (float, int)):
        return bool(value)
    if isinstance(value, bool):
        return value
    return False


def gravity_to_plato(gravity: float | None) -> float | None:
    """Convert specific gravity to degrees Plato using a polynomial approximation.

    Args:
        gravity: Specific gravity (e.g. ``1.050``).

    Returns:
        Degrees Plato, or ``None`` if ``gravity`` is ``None``.
    """
    if gravity is None:
        return None
    return (-463.37) + (668.72 * gravity) - (205.35 * (gravity * gravity))
