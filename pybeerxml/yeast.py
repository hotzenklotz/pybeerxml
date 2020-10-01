from typing import Optional, Text, Any

from pybeerxml.utils import cast_to_bool


class Yeast:
    def __init__(self):
        self.name: Optional[Text] = None
        self.version: Optional[int] = None
        self.type: Optional[Text] = None
        self.form: Optional[Text] = None  # May be "Liquid", "Dry", "Slant" or "Culture"
        self.attenuation: Optional[float] = None  # Percent
        self.notes: Optional[Text] = None
        self.laboratory: Optional[Text] = None
        self.product_id: Optional[Text] = None
        self.flocculation: Optional[
            Text
        ] = None  # May be "Low", "Medium", "High" or "Very High"
        self.amount: Optional[float] = None
        self._amount_is_weight: Optional[bool] = None
        self.min_temperature: Optional[float] = None
        self.max_temperature: Optional[float] = None
        self.best_for: Optional[Text] = None
        self.times_cultured: Optional[int] = None
        self.max_reuse: Optional[int] = None
        self._add_to_secondary: Optional[bool] = None
        self.inventory: Optional[Text] = None
        self.culture_date: Optional[Text] = None

    @property
    def amount_is_weight(self) -> Optional[bool]:
        if self._amount_is_weight is not None:
            return self._amount_is_weight

        return None

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        self._amount_is_weight = cast_to_bool(value)

    @property
    def add_to_secondary(self) -> Optional[bool]:
        if self._add_to_secondary is not None:
            return self._add_to_secondary

        return None

    @add_to_secondary.setter
    def add_to_secondary(self, value: Any):
        self._add_to_secondary = cast_to_bool(value)
