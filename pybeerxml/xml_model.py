from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import BeforeValidator, ConfigDict, PlainSerializer
from pydantic_xml import BaseXmlModel
from pydantic_xml.element.element import SearchMode

from pybeerxml.utils import cast_to_bool


def _serialize_beer_int(value: int) -> str:
    return str(value)


def _serialize_beer_float(value: float) -> str:
    text = format(Decimal(str(value)), "f")
    return text.rstrip("0").rstrip(".") or "0"


def _serialize_beer_bool(value: bool) -> str:
    return "TRUE" if value else "FALSE"


def _parse_int_or_str(value: object) -> object:
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def _parse_float_or_str(value: object) -> object:
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return value
    return value


def coerce_bool(value: bool | str | int | float | None) -> bool | None:
    """Coerce a BeerXML boolean-ish value to `bool | None`."""
    if value is None:
        return None
    return cast_to_bool(value)


def coerce_float(value: float | int | str | None) -> float | None:
    """Coerce a BeerXML numeric value to `float | None`."""
    if value is None:
        return None
    return float(value)


BeerInt = Annotated[int, PlainSerializer(_serialize_beer_int, return_type=str)]
BeerFloat = Annotated[float, PlainSerializer(_serialize_beer_float, return_type=str)]
BeerBool = Annotated[
    bool,
    BeforeValidator(cast_to_bool),
    PlainSerializer(_serialize_beer_bool, return_type=str),
]

IntOrStr = Annotated[
    int | str,
    BeforeValidator(_parse_int_or_str),
    PlainSerializer(lambda value: _serialize_beer_int(value) if isinstance(value, int) else value, return_type=str),
]
FloatOrStr = Annotated[
    float | str,
    BeforeValidator(_parse_float_or_str),
    PlainSerializer(lambda value: _serialize_beer_float(value) if isinstance(value, float) else value, return_type=str),
]


class BeerXmlModel(BaseXmlModel, search_mode=SearchMode.UNORDERED):
    """Base XML model with BeerXML-friendly scalar parsing.

    Model-specific compatibility aliases such as ``_yield`` or ``_og`` are
    implemented on the individual model classes where they are needed. Keeping
    those shims local avoids a global ``__setattr__``/``__getattr__`` hook that
    would otherwise interfere with normal descriptor and property behavior.
    """

    model_config = ConfigDict(extra="ignore", validate_assignment=True)
