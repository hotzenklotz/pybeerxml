from typing import Optional, Text, List
from pybeerxml.mash_step import MashStep
from pybeerxml.utils import cast_to_bool


class Mash:
    def __init__(self):
        self.name: Optional[Text] = None
        self.grain_temp: Optional[float] = None
        self.sparge_temp: Optional[float] = None
        # pylint: disable=invalid-name
        self.ph: Optional[float] = None
        self.notes: Optional[Text] = None
        self.name: Optional[Text] = None
        self.version: Optional[int] = None
        self.grain_temp: Optional[float] = None
        self.sparge_temp: Optional[float] = None
        self.ph: Optional[float] = None
        self.notes: Optional[Text] = None
        self.tun_temp: Optional[float] = None
        self.tun_weight: Optional[float] = None
        self.tun_specific_heat: Optional[float] = None
        self._equip_adjust: Optional[bool] = None

        self.steps: List[MashStep] = []

    @property
    def equip_adjust(self):
        return self._equip_adjust

    @equip_adjust.setter
    def equip_adjust(self, value):
        self._equip_adjust = cast_to_bool(value)
