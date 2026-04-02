from dataclasses import dataclass


@dataclass
class Water:
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

    name: str | None = None
    version: float | None = None
    amount: float | None = None
    calcium: float | None = None
    bicarbonate: float | None = None
    sulfate: float | None = None
    chloride: float | None = None
    sodium: float | None = None
    magnesium: float | None = None
    ph: float | None = None
    notes: str | None = None
    volume: float | None = None
