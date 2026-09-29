from pydantic_xml import element

from pybeerxml.base import BeerXmlModel, LenientFloat


class Water(BeerXmlModel, tag="WATER"):
    """Water chemistry profile from a BeerXML ``<WATER>`` element.

    All ion concentrations are in parts per million (ppm / mg/L).

    Attributes:
        name: Water profile name (e.g. ``"Burton on Trent"``).
        amount: Volume of water in litres.
        calcium: Calcium (Ca²⁺) concentration in ppm.
        bicarbonate: Bicarbonate (HCO₃⁻) concentration in ppm.
        sulfate: Sulfate (SO₄²⁻) concentration in ppm.
        chloride: Chloride (Cl⁻) concentration in ppm.
        sodium: Sodium (Na⁺) concentration in ppm.
        magnesium: Magnesium (Mg²⁺) concentration in ppm.
        ph: Water pH.
        notes: Free-text notes.
    """

    name: str | None = element(tag="NAME", default=None)
    version: int | None = element(tag="VERSION", default=None)
    amount: LenientFloat = element(tag="AMOUNT", default=None)
    calcium: LenientFloat = element(tag="CALCIUM", default=None)
    bicarbonate: LenientFloat = element(tag="BICARBONATE", default=None)
    sulfate: LenientFloat = element(tag="SULFATE", default=None)
    chloride: LenientFloat = element(tag="CHLORIDE", default=None)
    sodium: LenientFloat = element(tag="SODIUM", default=None)
    magnesium: LenientFloat = element(tag="MAGNESIUM", default=None)
    ph: LenientFloat = element(tag="PH", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    volume: LenientFloat = element(tag="VOLUME", default=None)
