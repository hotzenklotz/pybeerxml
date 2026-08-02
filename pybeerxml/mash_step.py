from pydantic_xml import element

from pybeerxml.base import BeerXmlModel, LenientFloat


class MashStep(BeerXmlModel, tag="MASH_STEP"):
    """A single temperature step within a mash profile.

    Attributes:
        name: Step name (e.g. ``"Dough In"``, ``"Conversion"``, ``"Mash Out"``).
        type: Step type — ``"Infusion"``, ``"Temperature"``, or ``"Decoction"``.
        infuse_amount: Volume of water infused in litres (infusion steps only).
        step_temp: Target step temperature in °C.
        end_temp: Final temperature at end of step in °C.
        step_time: Step duration in minutes.
        decoction_amt: Volume of mash removed for decoction (decoction steps only).
    """

    name: str | None = element(tag="NAME", default=None)
    type: str | None = element(tag="TYPE", default=None)
    infuse_amount: LenientFloat = element(tag="INFUSE_AMOUNT", default=None)
    step_temp: LenientFloat = element(tag="STEP_TEMP", default=None)
    end_temp: LenientFloat = element(tag="END_TEMP", default=None)
    step_time: LenientFloat = element(tag="STEP_TIME", default=None)
    decoction_amt: str | None = element(tag="DECOCTION_AMT", default=None)
    version: int | None = element(tag="VERSION", default=None)

    @property
    def water_ratio(self):
        """Water-to-grain ratio for this step. Not yet implemented."""
        raise NotImplementedError("water_ratio")
