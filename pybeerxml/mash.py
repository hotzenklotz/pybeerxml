from pydantic_xml import element, wrapped

from pybeerxml.base import BeerXmlModel, LenientFloat
from pybeerxml.mash_step import MashStep


class Mash(BeerXmlModel, tag="MASH"):
    """A mash profile, including temperature steps.

    Attributes:
        name: Profile name.
        grain_temp: Initial grain temperature in °C. Non-numeric XML values
            (e.g. ``"unknown"``) are kept as strings.
        sparge_temp: Sparge water temperature in °C.
        ph: Target mash pH.
        notes: Free-text notes.
        tun_temp: Mash tun temperature in °C.
        tun_weight: Mash tun weight in kg.
        tun_specific_heat: Specific heat of the mash tun material in Cal/(g·°C).
        equip_adjust: Whether mash temperatures are adjusted for equipment heat capacity.
        steps: Ordered list of mash temperature steps.
    """

    name: str | None = element(tag="NAME", default=None)
    version: int | None = element(tag="VERSION", default=None)
    grain_temp: LenientFloat = element(tag="GRAIN_TEMP", default=None)
    sparge_temp: LenientFloat = element(tag="SPARGE_TEMP", default=None)
    ph: LenientFloat = element(tag="PH", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    tun_temp: LenientFloat = element(tag="TUN_TEMP", default=None)
    tun_weight: LenientFloat = element(tag="TUN_WEIGHT", default=None)
    tun_specific_heat: LenientFloat = element(tag="TUN_SPECIFIC_HEAT", default=None)
    equip_adjust: bool | None = element(tag="EQUIP_ADJUST", default=None)
    steps: list[MashStep] = wrapped("MASH_STEPS", element(tag="MASH_STEP"), default_factory=list)
