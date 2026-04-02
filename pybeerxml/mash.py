from dataclasses import dataclass, field
from typing import Any

from pybeerxml.mash_step import MashStep
from pybeerxml.utils import cast_to_bool


@dataclass
class Mash:
    name: str | None = None
    version: int | None = None
    grain_temp: float | None = None
    sparge_temp: float | None = None
    ph: float | None = None
    notes: str | None = None
    tun_temp: float | None = None
    tun_weight: float | None = None
    tun_specific_heat: float | None = None
    steps: list[MashStep] = field(default_factory=list)
    _equip_adjust: bool | None = field(default=None, init=False, repr=False)

    @property
    def equip_adjust(self) -> bool | None:
        return self._equip_adjust

    @equip_adjust.setter
    def equip_adjust(self, value: Any) -> None:
        self._equip_adjust = cast_to_bool(value)
