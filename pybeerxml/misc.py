from typing import Any

from pybeerxml.utils import cast_to_bool


class Misc:
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

    def __init__(self):
        self.name: str | None = None
        self.version: int | None = None
        self.type: str | None = None
        self.amount: float | None = None
        self._amount_is_weight: bool | None = False
        self.use: str | None = None
        self.use_for: str | None = None
        self.time: float | None = None
        self.notes: str | None = None

    @property
    def amount_is_weight(self) -> bool | None:
        """``True`` if ``amount`` is measured by weight (kg), ``False`` if by volume (L)."""
        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        self._amount_is_weight = cast_to_bool(value)
