from dataclasses import dataclass, field
from typing import Any

from pybeerxml.mash_step import MashStep
from pybeerxml.utils import cast_to_bool


@dataclass
class Mash:
    """A mash profile, including temperature steps.

    Attributes:
        name: Profile name.
        grain_temp: Initial grain temperature in °C.
        sparge_temp: Sparge water temperature in °C.
        ph: Target mash pH.
        notes: Free-text notes.
        tun_temp: Mash tun temperature in °C.
        tun_weight: Mash tun weight in kg.
        tun_specific_heat: Specific heat of the mash tun material in Cal/(g·°C).
        steps: Ordered list of mash temperature steps.
    """

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
        """Whether mash temperatures are adjusted for equipment heat capacity."""
        return self._equip_adjust

    @equip_adjust.setter
    def equip_adjust(self, value: Any) -> None:
        self._equip_adjust = cast_to_bool(value)
