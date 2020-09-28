from typing import Optional, Text, Any
from pybeerxml.utils import cast_to_bool


class Misc:
    def __init__(self):
        self.name: Optional[Text] = None
        self.type: Optional[Text] = None
        self.amount: Optional[float] = None
        self._amount_is_weight: bool = False
        self.use: Optional[Text] = None
        self.use_for: Optional[Text] = None
        self.time: Optional[float] = None
        self.notes: Optional[Text] = None

    @property
    def amount_is_weight(self) -> bool:
        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        self._amount_is_weight = cast_to_bool(value)
