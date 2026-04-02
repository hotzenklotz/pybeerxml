class MashStep:
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

    def __init__(self):
        self.name: str | None = None
        self.type: str | None = None
        self.infuse_amount: float | None = None
        self.step_temp: float | None = None
        self.end_temp: float | None = None
        self.step_time: float | None = None
        self.decoction_amt: str | None = None
        self.version: int | None = None

    @property
    def water_ratio(self):
        """Water-to-grain ratio for this step. Not yet implemented."""
        raise NotImplementedError("water_ratio")
