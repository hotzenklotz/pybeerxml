from pydantic_xml import element, wrapped

from pybeerxml.mash_step import MashStep
from pybeerxml.xml_model import BeerBool, BeerFloat, BeerInt, BeerXmlModel, FloatOrStr


class Mash(BeerXmlModel, tag="MASH"):
    """A mash profile, including temperature steps.

    Attributes:
        name: Profile name.
        version: BeerXML mash profile version.
        grain_temp: Initial grain temperature in °C.
        sparge_temp: Sparge water temperature in °C.
        ph: Target mash pH.
        notes: Free-text notes.
        tun_temp: Mash tun temperature in °C.
        tun_weight: Mash tun weight in kg.
        tun_specific_heat: Specific heat of the mash tun material in Cal/(g·°C).
        steps: Ordered list of mash temperature steps.
    """

    name: str | None = element(tag="NAME", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    grain_temp: FloatOrStr | None = element(tag="GRAIN_TEMP", default=None)
    sparge_temp: BeerFloat | None = element(tag="SPARGE_TEMP", default=None)
    ph: BeerFloat | None = element(tag="PH", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    tun_temp: BeerFloat | None = element(tag="TUN_TEMP", default=None)
    tun_weight: BeerFloat | None = element(tag="TUN_WEIGHT", default=None)
    tun_specific_heat: BeerFloat | None = element(tag="TUN_SPECIFIC_HEAT", default=None)
    equip_adjust: BeerBool | None = element(tag="EQUIP_ADJUST", default=None)
    steps: list[MashStep] = wrapped("MASH_STEPS", element(tag="MASH_STEP", default_factory=list))
