from typing import Any

from pybeerxml.utils import cast_to_bool


class Equipment:
    def __init__(self):
        self.name: str | None = None
        self.version: str | None = None
        self.boil_size: float | None = None
        self.batch_size: float | None = None
        self.tun_volume: float | None = None
        self.tun_weight: float | None = None
        self.tun_specific_heat: float | None = None
        self.top_up_water: float | None = None
        self.trub_chiller_loss: float | None = None
        self.evap_rate: float | None = None
        self.boil_time: float | None = None
        self._calc_boil_volume: bool | None = None
        self.lauter_deadspace: float | None = None
        self.top_up_kettle: float | None = None
        self.hop_utilization: float | None = None
        self.notes: str | None = None

    @property
    def calc_boil_volume(self) -> bool | None:
        return self._calc_boil_volume

    @calc_boil_volume.setter
    def calc_boil_volume(self, value: Any):
        self._calc_boil_volume = cast_to_bool(value)
