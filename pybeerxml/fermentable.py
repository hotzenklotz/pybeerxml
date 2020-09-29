# pylint: disable=line-too-long
import re
import logging
from typing import Pattern, Text, Optional, List, Tuple

from pybeerxml.utils import cast_to_bool

logger = logging.getLogger(__name__)


STEEP = re.compile(
    re.compile(
        "/biscuit|black|cara|chocolate|crystal|munich|roast|special|toast|victory|vienna/i"
    )
)
BOIL = re.compile(
    re.compile("/candi|candy|dme|dry|extract|honey|lme|liquid|sugar|syrup|turbinado/i")
)


class Fermentable:
    # Regular expressions to match for boiling sugars (DME, LME, etc).

    def __init__(self):
        self.name: Optional[Text] = None
        self.amount: Optional[float] = None
        self._yield: Optional[float] = None
        self.color: Optional[float] = None
        self._add_after_boil: Optional[bool] = None  # Should be Bool
        self.version: Optional[int] = None
        self.type: Optional[Text] = None
        self.origin: Optional[Text] = None
        self.supplier: Optional[Text] = None
        self.notes: Optional[Text] = None
        self.coarse_fine_diff: Optional[float] = None
        self.moisture: Optional[float] = None
        self.diastatic_power: Optional[float] = None
        self.protein: Optional[float] = None
        self.max_in_batch: Optional[float] = None
        self._recommend_mash: Optional[bool] = None
        self.ibu_gal_per_lb: Optional[float] = None

    @property
    def add_after_boil(self) -> bool:
        return bool(self._add_after_boil)

    @add_after_boil.setter
    def add_after_boil(self, value):
        self._add_after_boil = value

    @property
    def ppg(self) -> Optional[float]:
        if self._yield is not None:
            return 0.46214 * self._yield

        logger.error(
            "Property 'ppg' could not be calculated because property 'yield' is missing. Default to 'None'"
        )
        return None

    @property
    def addition(self) -> Text:
        # When is this item added in the brewing process? Boil, steep, or mash?

        if self.name is None:
            logger.error(
                "Property 'addition' could not be calculated because property 'name' is missing. Defaults to 'mash'"
            )
            return "mash"

        regexes: List[Tuple[Pattern, Text]] = [
            # Forced values take precedence, then search known names and
            # default to mashing
            (re.compile("mash/i"), "mash"),
            (re.compile("steep/i"), "steep"),
            (re.compile("boil/i"), "boil"),
            (BOIL, "boil"),
            (STEEP, "steep"),
            (re.compile(".*"), "mash"),
        ]

        for regex, addition in regexes:
            try:
                if re.search(regex, self.name.lower()):
                    return addition
            except AttributeError:
                break

        return "mash"

    # pylint: disable=invalid-name
    def gu(self, liters: float = 1.0) -> Optional[float]:
        # Get the gravity units for a specific liquid volume with 100% efficiency
        if self.amount is None:
            logger.error(
                "Property 'gu' could not be calculated because property 'amount' is missing. Defaults to 'None'"
            )
            return None

        if self.ppg is None:
            logger.error(
                "Property 'gu' could not be calculated because property 'ppg' is missing. Defaults to 'None'"
            )
            return None

        # gu = parts per gallon * weight in pounds / gallons
        weight_lb = self.amount * 2.20462
        volume_gallons = liters * 0.264172
        return self.ppg * weight_lb / volume_gallons

    @property
    def recommend_mash(self):
        return self._recommend_mash

    @recommend_mash.setter
    def recommend_mash(self, value):
        self._recommend_mash = cast_to_bool(value)
