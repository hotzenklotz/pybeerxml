from pydantic_xml import element

from pybeerxml.base import BeerXmlModel, LenientFloat


class Equipment(BeerXmlModel, tag="EQUIPMENT"):
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
        calc_boil_volume: Whether the pre-boil volume should be calculated from
            equipment parameters.
        lauter_deadspace: Volume lost in the lauter tun in litres.
        top_up_kettle: Water added to the kettle before the boil in litres.
        hop_utilization: Global hop utilization multiplier (%).
        notes: Free-text notes.
    """

    name: str | None = element(tag="NAME", default=None)
    version: int | None = element(tag="VERSION", default=None)
    boil_size: LenientFloat = element(tag="BOIL_SIZE", default=None)
    batch_size: LenientFloat = element(tag="BATCH_SIZE", default=None)
    tun_volume: LenientFloat = element(tag="TUN_VOLUME", default=None)
    tun_weight: LenientFloat = element(tag="TUN_WEIGHT", default=None)
    tun_specific_heat: LenientFloat = element(tag="TUN_SPECIFIC_HEAT", default=None)
    top_up_water: LenientFloat = element(tag="TOP_UP_WATER", default=None)
    trub_chiller_loss: LenientFloat = element(tag="TRUB_CHILLER_LOSS", default=None)
    evap_rate: LenientFloat = element(tag="EVAP_RATE", default=None)
    boil_time: LenientFloat = element(tag="BOIL_TIME", default=None)
    calc_boil_volume: bool | None = element(tag="CALC_BOIL_VOLUME", default=None)
    lauter_deadspace: LenientFloat = element(tag="LAUTER_DEADSPACE", default=None)
    top_up_kettle: LenientFloat = element(tag="TOP_UP_KETTLE", default=None)
    hop_utilization: LenientFloat = element(tag="HOP_UTILIZATION", default=None)
    notes: str | None = element(tag="NOTES", default=None)
