from dataclasses import dataclass, field
from typing import Any

from pybeerxml.utils import cast_to_bool


@dataclass
class Equipment:
    name: str | None = None
    version: str | None = None
    boil_size: float | None = None
    batch_size: float | None = None
    tun_volume: float | None = None
    tun_weight: float | None = None
    tun_specific_heat: float | None = None
    top_up_water: float | None = None
    trub_chiller_loss: float | None = None
    evap_rate: float | None = None
    boil_time: float | None = None
    lauter_deadspace: float | None = None
    top_up_kettle: float | None = None
    hop_utilization: float | None = None
    notes: str | None = None
    _calc_boil_volume: bool | None = field(default=None, init=False, repr=False)

    @property
    def calc_boil_volume(self) -> bool | None:
        return self._calc_boil_volume

    @calc_boil_volume.setter
    def calc_boil_volume(self, value: Any) -> None:
        self._calc_boil_volume = cast_to_bool(value)
