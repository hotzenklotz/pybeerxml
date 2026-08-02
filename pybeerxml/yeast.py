from pydantic_xml import element

from pybeerxml.base import BeerXmlModel, LenientFloat, LenientInt


class Yeast(BeerXmlModel, tag="YEAST"):
    """A yeast strain used in a recipe.

    Attributes:
        name: Yeast strain name.
        type: Yeast type — ``"Ale"``, ``"Lager"``, ``"Wheat"``, ``"Wine"``, or ``"Champagne"``.
        form: Physical form — ``"Liquid"``, ``"Dry"``, ``"Slant"``, or ``"Culture"``.
        attenuation: Apparent attenuation percentage.
        laboratory: Producing laboratory (e.g. ``"Wyeast Labs"``).
        product_id: Laboratory product identifier. Numeric values are stored
            as ``int``; alphanumeric identifiers (e.g. ``"WLP001"``) stay strings.
        flocculation: Flocculation level — ``"Low"``, ``"Medium"``, ``"High"``, or ``"Very High"``.
        amount: Volume (litres) or weight (kg) of yeast used.
        amount_is_weight: ``True`` if ``amount`` is measured by weight (kg), ``False`` if by volume (L).
        add_to_secondary: ``True`` if this yeast is pitched at the secondary fermentation stage.
        min_temperature: Minimum recommended fermentation temperature in °C.
        max_temperature: Maximum recommended fermentation temperature in °C.
        best_for: Beer styles best suited to this strain.
        notes: Free-text notes.
    """

    name: str | None = element(tag="NAME", default=None)
    version: int | None = element(tag="VERSION", default=None)
    type: str | None = element(tag="TYPE", default=None)
    form: str | None = element(tag="FORM", default=None)
    attenuation: float | None = element(tag="ATTENUATION", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    laboratory: str | None = element(tag="LABORATORY", default=None)
    product_id: LenientInt = element(tag="PRODUCT_ID", default=None)
    flocculation: str | None = element(tag="FLOCCULATION", default=None)
    amount: LenientFloat = element(tag="AMOUNT", default=None)
    min_temperature: LenientFloat = element(tag="MIN_TEMPERATURE", default=None)
    max_temperature: LenientFloat = element(tag="MAX_TEMPERATURE", default=None)
    best_for: str | None = element(tag="BEST_FOR", default=None)
    times_cultured: int | None = element(tag="TIMES_CULTURED", default=None)
    max_reuse: int | None = element(tag="MAX_REUSE", default=None)
    inventory: str | None = element(tag="INVENTORY", default=None)
    culture_date: str | None = element(tag="CULTURE_DATE", default=None)
    amount_is_weight: bool | None = element(tag="AMOUNT_IS_WEIGHT", default=None)
    add_to_secondary: bool | None = element(tag="ADD_TO_SECONDARY", default=None)
