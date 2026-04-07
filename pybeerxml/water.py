from pydantic_xml import element

from pybeerxml.xml_model import BeerFloat, BeerInt, BeerXmlModel


class Water(BeerXmlModel, tag="WATER"):
    """Water chemistry profile from a BeerXML ``<WATER>`` element.

    All ion concentrations are in parts per million (ppm / mg/L).

    Attributes:
        name: Water profile name (e.g. ``"Burton on Trent"``).
        version: BeerXML water profile version.
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
    version: BeerInt | None = element(tag="VERSION", default=None)
    amount: BeerFloat | None = element(tag="AMOUNT", default=None)
    calcium: BeerFloat | None = element(tag="CALCIUM", default=None)
    bicarbonate: BeerFloat | None = element(tag="BICARBONATE", default=None)
    sulfate: BeerFloat | None = element(tag="SULFATE", default=None)
    chloride: BeerFloat | None = element(tag="CHLORIDE", default=None)
    sodium: BeerFloat | None = element(tag="SODIUM", default=None)
    magnesium: BeerFloat | None = element(tag="MAGNESIUM", default=None)
    ph: BeerFloat | None = element(tag="PH", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    volume: BeerFloat | None = element(tag="VOLUME", default=None)
