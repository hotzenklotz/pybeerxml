from dataclasses import dataclass, field
from typing import Any

from pybeerxml.utils import cast_to_bool


@dataclass
class Yeast:
    name: str | None = None
    version: int | None = None
    type: str | None = None
    form: str | None = None  # May be "Liquid", "Dry", "Slant" or "Culture"
    attenuation: float | None = None  # Percent
    notes: str | None = None
    laboratory: str | None = None
    product_id: str | None = None
    flocculation: str | None = None  # May be "Low", "Medium", "High" or "Very High"
    amount: float | None = None
    min_temperature: float | None = None
    max_temperature: float | None = None
    best_for: str | None = None
    times_cultured: int | None = None
    max_reuse: int | None = None
    inventory: str | None = None
    culture_date: str | None = None
    _amount_is_weight: bool | None = field(default=None, init=False, repr=False)
    _add_to_secondary: bool | None = field(default=None, init=False, repr=False)

    @property
    def amount_is_weight(self) -> bool | None:
        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any) -> None:
        self._amount_is_weight = cast_to_bool(value)

    @property
    def add_to_secondary(self) -> bool | None:
        return self._add_to_secondary

    @add_to_secondary.setter
    def add_to_secondary(self, value: Any) -> None:
        self._add_to_secondary = cast_to_bool(value)
