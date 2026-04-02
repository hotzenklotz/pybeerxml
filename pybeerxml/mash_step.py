class MashStep:
    def __init__(self):
        self.name: str | None = None
        self.type: str | None = None  # May be "Infusion", "Temperature" or "Decoction"
        self.infuse_amount: float | None = None  # liters
        self.step_temp: float | None = None  # temperature (should be Celsius)
        self.end_temp: float | None = None  # temperature (should be Celsius)
        self.step_time: float | None = None  # time in minutes
        self.decoction_amt: str | None = None
        self.version: int | None = None

    @property
    def water_ratio(self):
        raise NotImplementedError("water_ratio")
        # water_amout = self.infuse_amount or self.decoction_amt
        # return water_amount / recipe.grainWeight()
