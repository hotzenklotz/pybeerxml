import logging
import re
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


class Fermentable:
    def __init__(self):
        self.name: str | None = None
        self.amount: float | None = None
        self._yield: float | None = None
        self.color: float | None = None
        self._add_after_boil: bool | None = None
        self.version: int | None = None
        self.type: str | None = None
        self.origin: str | None = None
        self.supplier: str | None = None
        self.notes: str | None = None
        self.coarse_fine_diff: float | None = None
        self.moisture: float | None = None
        self.diastatic_power: float | None = None
        self.protein: float | None = None
        self.max_in_batch: float | None = None
        self._recommend_mash: bool | None = None
        self.ibu_gal_per_lb: float | None = None

    @property
    def add_after_boil(self) -> bool:
        return bool(self._add_after_boil)

    @add_after_boil.setter
    def add_after_boil(self, value: Any):
        self._add_after_boil = cast_to_bool(value)

    @property
    def ppg(self) -> float | None:
        if self._yield is not None:
            return 0.46214 * self._yield
        logger.error("Property 'ppg' could not be calculated because property 'yield' is missing. Default to 'None'")
        return None

    @property
    def addition(self) -> str:
        "Determine when this fermentable is added: 'mash', 'steep', or 'boil'."
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
        "Get the gravity units for a specific liquid volume with 100% efficiency."
        if self.amount is None:
            logger.error(
                "Property 'gu' could not be calculated because property 'amount' is missing. Defaults to 'None'"
            )
            return None
        if self.ppg is None:
            logger.error("Property 'gu' could not be calculated because property 'ppg' is missing. Defaults to 'None'")
            return None
        # gu = parts per gallon * weight in pounds / gallons
        weight_lb = self.amount * 2.20462
        volume_gallons = liters * 0.264172
        return self.ppg * weight_lb / volume_gallons

    @property
    def recommend_mash(self) -> bool | None:
        return self._recommend_mash

    @recommend_mash.setter
    def recommend_mash(self, value: Any):
        self._recommend_mash = cast_to_bool(value)
