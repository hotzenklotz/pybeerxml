from pydantic_xml import element

from pybeerxml.xml_model import BeerBool, BeerFloat, BeerInt, BeerXmlModel


class Equipment(BeerXmlModel, tag="EQUIPMENT"):
    """Brewing equipment profile from a BeerXML ``<EQUIPMENT>`` element.

    Attributes:
        name: Equipment set name.
        version: BeerXML equipment profile version.
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

    name: str | None = element(tag="NAME", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    boil_size: BeerFloat | None = element(tag="BOIL_SIZE", default=None)
    batch_size: BeerFloat | None = element(tag="BATCH_SIZE", default=None)
    tun_volume: BeerFloat | None = element(tag="TUN_VOLUME", default=None)
    tun_weight: BeerFloat | None = element(tag="TUN_WEIGHT", default=None)
    tun_specific_heat: BeerFloat | None = element(tag="TUN_SPECIFIC_HEAT", default=None)
    top_up_water: BeerFloat | None = element(tag="TOP_UP_WATER", default=None)
    trub_chiller_loss: BeerFloat | None = element(tag="TRUB_CHILLER_LOSS", default=None)
    evap_rate: BeerFloat | None = element(tag="EVAP_RATE", default=None)
    boil_time: BeerFloat | None = element(tag="BOIL_TIME", default=None)
    calc_boil_volume: BeerBool | None = element(tag="CALC_BOIL_VOLUME", default=None)
    lauter_deadspace: BeerFloat | None = element(tag="LAUTER_DEADSPACE", default=None)
    top_up_kettle: BeerFloat | None = element(tag="TOP_UP_KETTLE", default=None)
    hop_utilization: BeerFloat | None = element(tag="HOP_UTILIZATION", default=None)
    notes: str | None = element(tag="NOTES", default=None)
