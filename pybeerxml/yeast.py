from typing import Any

from pybeerxml.utils import cast_to_bool


class Yeast:
    def __init__(self):
        self.name: str | None = None
        self.version: int | None = None
        self.type: str | None = None
        self.form: str | None = None  # May be "Liquid", "Dry", "Slant" or "Culture"
        self.attenuation: float | None = None  # Percent
        self.notes: str | None = None
        self.laboratory: str | None = None
        self.product_id: str | None = None
        self.flocculation: str | None = None  # May be "Low", "Medium", "High" or "Very High"
        self.amount: float | None = None
        self._amount_is_weight: bool | None = None
        self.min_temperature: float | None = None
        self.max_temperature: float | None = None
        self.best_for: str | None = None
        self.times_cultured: int | None = None
        self.max_reuse: int | None = None
        self._add_to_secondary: bool | None = None
        self.inventory: str | None = None
        self.culture_date: str | None = None

    @property
    def amount_is_weight(self) -> bool | None:
        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        self._amount_is_weight = cast_to_bool(value)

    @property
    def add_to_secondary(self) -> bool | None:
        return self._add_to_secondary

    @add_to_secondary.setter
    def add_to_secondary(self, value: Any):
        self._add_to_secondary = cast_to_bool(value)
