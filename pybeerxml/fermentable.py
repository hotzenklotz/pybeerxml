import logging
import re

from pydantic_xml import element

from pybeerxml.xml_model import BeerBool, BeerFloat, BeerInt, BeerXmlModel

logger = logging.getLogger(__name__)

# Patterns to detect how a fermentable is added during brewing.
# Forced keyword overrides (name explicitly contains "mash", "steep", or "boil") take precedence,
# then known ingredient name patterns are checked, defaulting to mash.
_FORCE_MASH = re.compile(r"mash", re.IGNORECASE)
_FORCE_STEEP = re.compile(r"steep", re.IGNORECASE)
_FORCE_BOIL = re.compile(r"boil", re.IGNORECASE)
STEEP = re.compile(r"biscuit|black|cara|chocolate|crystal|munich|roast|special|toast|victory|vienna", re.IGNORECASE)
BOIL = re.compile(r"candi|candy|dme|dry|extract|honey|lme|liquid|sugar|syrup|turbinado", re.IGNORECASE)


class Fermentable(BeerXmlModel, tag="FERMENTABLE"):
    """A fermentable ingredient — grain, extract, sugar, or adjunct.

    Attributes:
        name: Ingredient name.
        amount: Weight in kilograms.
        color: Colour contribution in degrees Lovibond (°L).
        version: BeerXML fermentable record version.
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

    name: str | None = element(tag="NAME", default=None)
    amount: BeerFloat | None = element(tag="AMOUNT", default=None)
    color: BeerFloat | None = element(tag="COLOR", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    type: str | None = element(tag="TYPE", default=None)
    origin: str | None = element(tag="ORIGIN", default=None)
    supplier: str | None = element(tag="SUPPLIER", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    coarse_fine_diff: BeerFloat | None = element(tag="COARSE_FINE_DIFF", default=None)
    moisture: BeerFloat | None = element(tag="MOISTURE", default=None)
    diastatic_power: BeerFloat | None = element(tag="DIASTATIC_POWER", default=None)
    protein: BeerFloat | None = element(tag="PROTEIN", default=None)
    max_in_batch: BeerFloat | None = element(tag="MAX_IN_BATCH", default=None)
    ibu_gal_per_lb: BeerFloat | None = element(tag="IBU_GAL_PER_LB", default=None)
    yield_pct: BeerFloat | None = element(tag="YIELD", default=None)
    add_after_boil: BeerBool | None = element(tag="ADD_AFTER_BOIL", default=False)
    recommend_mash: BeerBool | None = element(tag="RECOMMEND_MASH", default=None)

    @property
    def _yield(self) -> float | None:
        return self.yield_pct

    @_yield.setter
    def _yield(self, value: float | int | str | None) -> None:
        self.yield_pct = value

    @property
    def _add_after_boil(self) -> bool | None:
        return self.add_after_boil

    @_add_after_boil.setter
    def _add_after_boil(self, value: bool | str | int | float | None) -> None:
        self.add_after_boil = value

    @property
    def _recommend_mash(self) -> bool | None:
        return self.recommend_mash

    @_recommend_mash.setter
    def _recommend_mash(self, value: bool | str | int | float | None) -> None:
        self.recommend_mash = value

    @property
    def ppg(self) -> float | None:
        """Points per pound per gallon, derived from the BeerXML ``YIELD`` field.

        Returns ``None`` when ``YIELD`` is not set.
        """
        if self.yield_pct is not None:
            return 0.46214 * self.yield_pct
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
