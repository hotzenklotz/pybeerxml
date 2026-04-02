import logging
import re
from dataclasses import dataclass, field
from typing import Any

from pybeerxml.utils import cast_to_bool

logger = logging.getLogger(__name__)

# Patterns to detect how a fermentable is added during brewing.
# Forced keyword overrides (name explicitly contains "mash", "steep", or "boil") take precedence,
# then known ingredient name patterns are checked, defaulting to mash.
_FORCE_MASH = re.compile(r"mash", re.IGNORECASE)
_FORCE_STEEP = re.compile(r"steep", re.IGNORECASE)
_FORCE_BOIL = re.compile(r"boil", re.IGNORECASE)
STEEP = re.compile(r"biscuit|black|cara|chocolate|crystal|munich|roast|special|toast|victory|vienna", re.IGNORECASE)
BOIL = re.compile(r"candi|candy|dme|dry|extract|honey|lme|liquid|sugar|syrup|turbinado", re.IGNORECASE)


@dataclass
class Fermentable:
    """A fermentable ingredient — grain, extract, sugar, or adjunct.

    Attributes:
        name: Ingredient name.
        amount: Weight in kilograms.
        color: Colour contribution in degrees Lovibond (°L).
        type: Ingredient type (e.g. ``"Grain"``, ``"Extract"``, ``"Sugar"``).
        origin: Country of origin.
        supplier: Supplier or maltster name.
        notes: Free-text notes.
        coarse_fine_diff: Difference between coarse and fine grind yield (%).
        moisture: Moisture content (%).
        diastatic_power: Diastatic power in degrees Lintner.
        protein: Protein content (%).
        max_in_batch: Maximum recommended percentage of the grain bill.
        ibu_gal_per_lb: IBU contribution per gallon per pound (for adjuncts).
    """

    name: str | None = None
    amount: float | None = None
    color: float | None = None
    version: int | None = None
    type: str | None = None
    origin: str | None = None
    supplier: str | None = None
    notes: str | None = None
    coarse_fine_diff: float | None = None
    moisture: float | None = None
    diastatic_power: float | None = None
    protein: float | None = None
    max_in_batch: float | None = None
    ibu_gal_per_lb: float | None = None
    # "yield" is a Python keyword, so the parser maps it to _yield via setattr
    _yield: float | None = field(default=None, init=False, repr=False)
    _add_after_boil: bool | None = field(default=None, init=False, repr=False)
    _recommend_mash: bool | None = field(default=None, init=False, repr=False)

    @property
    def add_after_boil(self) -> bool:
        """Whether this fermentable is added after the boil (e.g. honey in secondary)."""
        return bool(self._add_after_boil)

    @add_after_boil.setter
    def add_after_boil(self, value: Any) -> None:
        self._add_after_boil = cast_to_bool(value)

    @property
    def ppg(self) -> float | None:
        """Points per pound per gallon, derived from the BeerXML ``YIELD`` field.

        Returns ``None`` when ``YIELD`` is not set.
        """
        if self._yield is not None:
            return 0.46214 * self._yield
        logger.error("Property 'ppg' could not be calculated because property 'yield' is missing. Default to 'None'")
        return None

    @property
    def addition(self) -> str:
        """When this fermentable is added during the brewing process.

        Returns one of ``"mash"``, ``"steep"``, or ``"boil"``, determined by
        matching the ingredient name against known patterns.  Explicit keywords
        in the name (``"mash"``, ``"steep"``, ``"boil"``) take precedence over
        pattern matching.  Unknown ingredients default to ``"mash"``.
        """
        if self.name is None:
            logger.error(
                "Property 'addition' could not be calculated because property 'name' is missing. Defaults to 'mash'"
            )
            return "mash"
        if _FORCE_MASH.search(self.name):
            return "mash"
        if _FORCE_STEEP.search(self.name):
            return "steep"
        if _FORCE_BOIL.search(self.name):
            return "boil"
        if BOIL.search(self.name):
            return "boil"
        if STEEP.search(self.name):
            return "steep"
        return "mash"

    def gu(self, liters: float = 1.0) -> float | None:
        """Gravity units contributed at 100 % efficiency for the given volume.

        Args:
            liters: Batch volume in litres.

        Returns:
            Gravity units as a float, or ``None`` if ``amount`` or ``yield``
            is not set.
        """
        if self.amount is None:
            logger.error(
                "Property 'gu' could not be calculated because property 'amount' is missing. Defaults to 'None'"
            )
            return None
        if self.ppg is None:
            logger.error("Property 'gu' could not be calculated because property 'ppg' is missing. Defaults to 'None'")
            return None
        weight_lb = self.amount * 2.20462
        volume_gallons = liters * 0.264172
        return self.ppg * weight_lb / volume_gallons

    @property
    def recommend_mash(self) -> bool | None:
        """Whether mashing is recommended for this fermentable."""
        return self._recommend_mash

    @recommend_mash.setter
    def recommend_mash(self, value: Any) -> None:
        self._recommend_mash = cast_to_bool(value)
