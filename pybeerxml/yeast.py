from pydantic_xml import element

from pybeerxml.xml_model import BeerBool, BeerFloat, BeerInt, BeerXmlModel, IntOrStr


class Yeast(BeerXmlModel, tag="YEAST"):
    """A yeast strain used in a recipe.

    Attributes:
        name: Yeast strain name.
        version: BeerXML yeast record version.
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

    name: str | None = element(tag="NAME", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    type: str | None = element(tag="TYPE", default=None)
    form: str | None = element(tag="FORM", default=None)
    attenuation: BeerFloat | None = element(tag="ATTENUATION", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    laboratory: str | None = element(tag="LABORATORY", default=None)
    product_id: IntOrStr | None = element(tag="PRODUCT_ID", default=None)
    flocculation: str | None = element(tag="FLOCCULATION", default=None)
    amount: BeerFloat | None = element(tag="AMOUNT", default=None)
    min_temperature: BeerFloat | None = element(tag="MIN_TEMPERATURE", default=None)
    max_temperature: BeerFloat | None = element(tag="MAX_TEMPERATURE", default=None)
    best_for: str | None = element(tag="BEST_FOR", default=None)
    times_cultured: BeerInt | None = element(tag="TIMES_CULTURED", default=None)
    max_reuse: BeerInt | None = element(tag="MAX_REUSE", default=None)
    inventory: str | None = element(tag="INVENTORY", default=None)
    culture_date: str | None = element(tag="CULTURE_DATE", default=None)
    amount_is_weight: BeerBool | None = element(tag="AMOUNT_IS_WEIGHT", default=None)
    add_to_secondary: BeerBool | None = element(tag="ADD_TO_SECONDARY", default=None)
