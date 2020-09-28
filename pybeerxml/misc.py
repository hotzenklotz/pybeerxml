from typing import Optional, Text, Any
from pybeerxml.utils import cast_to_bool


class Misc:
    def __init__(self):
        self.name: Optional[Text] = None
        self.type: Optional[Text] = None
        self.amount: Optional[float] = None
        self._amount_is_weight: Optional[bool] = False
        self.use: Optional[Text] = None
        self.use_for: Optional[Text] = None
        self.time: Optional[float] = None
        self.notes: Optional[Text] = None

    @property
    def amount_is_weight(self) -> Optional[bool]:
        if self._amount_is_weight is not None:
            return self._amount_is_weight

        return None

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        self._amount_is_weight = cast_to_bool(value)
