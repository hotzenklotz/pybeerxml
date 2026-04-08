from pydantic_xml import element

from pybeerxml.xml_model import BeerBool, BeerFloat, BeerInt, BeerXmlModel


class Misc(BeerXmlModel, tag="MISC"):
    """A miscellaneous ingredient — finings, spices, water agents, etc.

    Attributes:
        name: Ingredient name.
        version: BeerXML misc record version.
        type: Category — ``"Spice"``, ``"Fining"``, ``"Water Agent"``,
            ``"Herb"``, ``"Flavor"``, or ``"Other"``.
        amount: Quantity — weight in kg or volume in litres depending on
            ``amount_is_weight``.
        use: When the ingredient is added — ``"Boil"``, ``"Mash"``,
            ``"Primary"``, ``"Secondary"``, or ``"Bottling"``.
        use_for: Description of the ingredient's purpose.
        time: Contact time in minutes.
        notes: Free-text notes.
    """

    name: str | None = element(tag="NAME", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    type: str | None = element(tag="TYPE", default=None)
    amount: BeerFloat | None = element(tag="AMOUNT", default=None)
    amount_is_weight: BeerBool | None = element(tag="AMOUNT_IS_WEIGHT", default=False)
    use: str | None = element(tag="USE", default=None)
    use_for: str | None = element(tag="USE_FOR", default=None)
    time: BeerFloat | None = element(tag="TIME", default=None)
    notes: str | None = element(tag="NOTES", default=None)
