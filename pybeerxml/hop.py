import math

from pydantic_xml import element

from pybeerxml.xml_model import BeerFloat, BeerInt, BeerXmlModel


class Hop(BeerXmlModel, tag="HOP"):
    """A hop addition in a beer recipe.

    Attributes:
        name: Hop variety name.
        alpha: Alpha acid percentage.
        amount: Weight in kilograms.
        use: When the hop is added — ``"boil"``, ``"dry hop"``, ``"aroma"``, etc.
        form: Physical form — ``"pellet"``, ``"whole"``, or ``"plug"``.
        time: Contact time in minutes (boil time, dry-hop duration, etc.).
        type: Hop type — ``"bittering"``, ``"aroma"``, or ``"both"``.
        beta: Beta acid percentage.
        origin: Country of origin.
        notes: Free-text notes.
    """

    name: str | None = element(tag="NAME", default=None)
    alpha: BeerFloat | None = element(tag="ALPHA", default=None)
    amount: BeerFloat | None = element(tag="AMOUNT", default=None)
    use: str | None = element(tag="USE", default=None)
    form: str | None = element(tag="FORM", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    time: BeerFloat | None = element(tag="TIME", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    type: str | None = element(tag="TYPE", default=None)
    beta: BeerFloat | None = element(tag="BETA", default=None)
    hsi: BeerFloat | None = element(tag="HSI", default=None)
    origin: str | None = element(tag="ORIGIN", default=None)
    substitutes: str | None = element(tag="SUBSTITUTES", default=None)
    humulene: BeerFloat | None = element(tag="HUMULENE", default=None)
    caryophyllene: BeerFloat | None = element(tag="CARYOPHYLLENE", default=None)
    cohumulone: BeerFloat | None = element(tag="COHUMULONE", default=None)
    myrcene: BeerFloat | None = element(tag="MYRCENE", default=None)

    def utilization_factor(self) -> float:
        """Utilization multiplier for hop form.

        Pellet hops are approximately 15 % more efficient than whole hops.

        Returns:
            ``1.15`` for pellets, ``1.0`` for all other forms.
        """
        return 1.15 if self.form == "pellet" else 1.0

    def bitterness(self, ibu_method: str, early_og: float, batch_size: float) -> float:
        """Calculate the IBU contribution of this hop addition.

        Args:
            ibu_method: Formula to use — ``"tinseth"`` or ``"rager"``.
            early_og: Original gravity at the start of the boil (e.g. ``1.050``).
            batch_size: Batch volume in litres.

        Returns:
            IBU contribution as a float.

        Raises:
            ValueError: If ``time``, ``alpha``, or ``amount`` is ``None``.
            ValueError: If ``ibu_method`` is not ``"tinseth"`` or ``"rager"``.
        """
        if self.time is None or self.alpha is None or self.amount is None:
            raise ValueError("Hop is missing required fields (time, alpha, amount) for bitterness calculation")

        if ibu_method == "tinseth":
            return (
                1.65
                * math.pow(0.000125, early_og - 1.0)
                * ((1 - math.pow(math.e, -0.04 * self.time)) / 4.15)
                * ((self.alpha / 100.0 * self.amount * 1000000) / batch_size)
                * self.utilization_factor()
            )

        if ibu_method == "rager":
            utilization = 18.11 + 13.86 * math.tanh((self.time - 31.32) / 18.27)
            adjustment = max(0, (early_og - 1.050) / 0.2)
            return (
                self.amount
                * 100
                * utilization
                * self.utilization_factor()
                * self.alpha
                / (batch_size * (1 + adjustment))
            )

        raise ValueError(f"Unknown IBU method: {ibu_method!r}")
