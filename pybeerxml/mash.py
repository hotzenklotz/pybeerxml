from typing import Any

from pybeerxml.mash_step import MashStep
from pybeerxml.utils import cast_to_bool


class Mash:
    def __init__(self):
        self.name: str | None = None
        self.version: int | None = None
        self.grain_temp: float | None = None
        self.sparge_temp: float | None = None
        self.ph: float | None = None
        self.notes: str | None = None
        self.tun_temp: float | None = None
        self.tun_weight: float | None = None
        self.tun_specific_heat: float | None = None
        self._equip_adjust: bool | None = None
        self.steps: list[MashStep] = []

    @property
    def equip_adjust(self) -> bool | None:
        return self._equip_adjust

    @equip_adjust.setter
    def equip_adjust(self, value: Any):
        self._equip_adjust = cast_to_bool(value)
