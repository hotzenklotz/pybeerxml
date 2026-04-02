from typing import Any

from pybeerxml.utils import cast_to_bool


class Misc:
    def __init__(self):
        self.name: str | None = None
        self.type: str | None = None
        self.amount: float | None = None
        self._amount_is_weight: bool | None = False
        self.use: str | None = None
        self.use_for: str | None = None
        self.time: float | None = None
        self.notes: str | None = None

    @property
    def amount_is_weight(self) -> bool | None:
        return self._amount_is_weight

    @amount_is_weight.setter
    def amount_is_weight(self, value: Any):
        self._amount_is_weight = cast_to_bool(value)
