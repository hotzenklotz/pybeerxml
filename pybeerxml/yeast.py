from dataclasses import dataclass, field
from typing import Any

from pybeerxml.utils import cast_to_bool


@dataclass
class Yeast:
    """A yeast strain used in a recipe.

    Attributes:
        name: Yeast strain name.
        type: Yeast type — ``"Ale"``, ``"Lager"``, ``"Wheat"``, ``"Wine"``, or ``"Champagne"``.
        form: Physical form — ``"Liquid"``, ``"Dry"``, ``"Slant"``, or ``"Culture"``.
        attenuation: Apparent attenuation percentage.
        laboratory: Producing laboratory (e.g. ``"Wyeast Labs"``).
        product_id: Laboratory product identifier.
        flocculation: Flocculation level — ``"Low"``, ``"Medium"``, ``"High"``, or ``"Very High"``.
        amount: Volume (litres) or weight (kg) of yeast used.
        min_temperature: Minimum recommended fermentation temperature in °C.
        max_temperature: Maximum recommended fermentation temperature in °C.
        best_for: Beer styles best suited to this strain.
        notes: Free-text notes.
    """

    name: str | None = None
    version: int | None = None
    type: str | None = None
    form: str | None = None
    attenuation: float | None = None
    notes: str | None = None
    laboratory: str | None = None
    product_id: str | None = None
    flocculation: str | None = None
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
        """``True`` if ``amount`` is measured by weight (kg), ``False`` if by volume (L)."""
        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any) -> None:
        self._amount_is_weight = cast_to_bool(value)

    @property
    def add_to_secondary(self) -> bool | None:
        """``True`` if this yeast is pitched at the secondary fermentation stage."""
        return self._add_to_secondary

    @add_to_secondary.setter
    def add_to_secondary(self, value: Any) -> None:
        self._add_to_secondary = cast_to_bool(value)
