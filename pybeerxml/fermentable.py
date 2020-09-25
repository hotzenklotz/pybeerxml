import re
from typing import Text, Optional


class Fermentable:
    # Regular expressions to match for boiling sugars (DME, LME, etc).
    STEEP = re.compile(
        "/biscuit|black|cara|chocolate|crystal|munich|roast|special|toast|victory|vienna/i"
    )
    BOIL = re.compile(
        "/candi|candy|dme|dry|extract|honey|lme|liquid|sugar|syrup|turbinado/i"
    )

    def __init__(self):
        self.name: Optional[Text] = None
        self.amount: Optional[float] = None
        self._yield: Optional[float] = None
        self.color: Optional[float] = None
        self._add_after_boil: Optional[bool] = None  # Should be Bool

    @property
    def add_after_boil(self) -> bool:
        return bool(self._add_after_boil)

    @add_after_boil.setter
    def add_after_boil(self, value):
        self._add_after_boil = value

    @property
    def ppg(self) -> float:
        return 0.46214 * self._yield

    @property
    def addition(self) -> Text:
        # When is this item added in the brewing process? Boil, steep, or mash?

        regexes = [
            # Forced values take precedence, then search known names and
            # default to mashing
            [re.compile("mash/i"), "mash"],
            [re.compile("steep/i"), "steep"],
            [re.compile("boil/i"), "boil"],
            [Fermentable.BOIL, "boil"],
            [Fermentable.STEEP, "steep"],
            [re.compile(".*"), "mash"],
        ]

        for regex, addition in regexes:
            try:
                if re.search(regex, self.name.lower()):
                    return addition
            except AttributeError:
                break

        return "mash"

    def gu(self, liters: float = 1.0) -> float:
        # Get the gravity units for a specific liquid volume with 100% efficiency

        # gu = parts per gallon * weight in pounds / gallons
        weight_lb = self.amount * 2.20462
        volume_gallons = liters * 0.264172
        return self.ppg * weight_lb / volume_gallons
