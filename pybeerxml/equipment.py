from typing import Any, Optional, Text
from pybeerxml.utils import cast_to_bool


class Equipment:
    def __init__(self):
        self.name: Optional[Text] = None
        self.version: Optional[Text] = None
        self.boil_size: Optional[float] = None
        self.batch_size: Optional[float] = None
        self.tun_volume: Optional[float] = None
        self.tun_weight: Optional[float] = None
        self.tun_specific_heat: Optional[float] = None
        self.top_up_water: Optional[float] = None
        self.trub_chiller_loss: Optional[float] = None
        self.evap_rate: Optional[float] = None
        self.boil_time: Optional[float] = None
        self._calc_boil_volume: Optional[bool] = None
        self.lauter_deadspace: Optional[float] = None
        self.top_up_kettle: Optional[float] = None
        self.hop_utilization: Optional[float] = None
        self.notes: Optional[Text] = None

    @property
    def calc_boil_volume(self) -> Optional[bool]:
        if self._calc_boil_volume is not None:
            return self._calc_boil_volume

        return None

    @calc_boil_volume.setter
    def calc_boil_volume(self, value: Any):
        self._calc_boil_volume = cast_to_bool(value)
