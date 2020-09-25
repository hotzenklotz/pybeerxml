from typing import Optional, Text, Any


class Misc:
    def __init__(self):
        self.name: Optional[Text] = None
        self.type: Optional[Text] = None
        self.amount: Optional[float] = None
        self._amount_is_weight: Optional[bool] = None
        self.use: Optional[Text] = None
        self.use_for: Optional[Text] = None
        self.time: Optional[float] = None
        self.notes: Optional[Text] = None

    @property
    def amount_is_weight(self) -> bool:

        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        if isinstance(value, str):
            self._amount_is_weight = value.lower() == "true"
        elif isinstance(value, (float, int)):
            self._amount_is_weight = bool(value)
        elif isinstance(value, bool):
            self._amount_is_weight = value

        return False