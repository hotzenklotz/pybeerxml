from dataclasses import dataclass, field
from typing import Any

from pybeerxml.utils import cast_to_bool


@dataclass
class Equipment:
    """Brewing equipment profile from a BeerXML ``<EQUIPMENT>`` element.

    Attributes:
        name: Equipment set name.
        boil_size: Pre-boil kettle volume in litres.
        batch_size: Target post-boil batch volume in litres.
        tun_volume: Mash tun capacity in litres.
        tun_weight: Mash tun weight in kg (used for heat loss calculations).
        tun_specific_heat: Specific heat of the tun material in Cal/(g·°C).
        top_up_water: Water added to the fermenter to reach ``batch_size`` in litres.
        trub_chiller_loss: Volume lost to trub and chiller deadspace in litres.
        evap_rate: Evaporation rate in litres per hour.
        boil_time: Boil duration in minutes.
        lauter_deadspace: Volume lost in the lauter tun in litres.
        top_up_kettle: Water added to the kettle before the boil in litres.
        hop_utilization: Global hop utilization multiplier (%).
        notes: Free-text notes.
    """

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
        """Whether the pre-boil volume should be calculated from equipment parameters."""
        return self._calc_boil_volume

    @calc_boil_volume.setter
    def calc_boil_volume(self, value: Any) -> None:
        self._calc_boil_volume = cast_to_bool(value)
