from typing import Optional, Text


class MashStep:
    def __init__(self):
        self.name: Optional[Text] = None
        self.type: Optional[
            Text
        ] = None  # May be "Infusion", "Temperature" or "Decoction"
        self.infuse_amount: Optional[float] = None  # liters
        self.step_temp: Optional[float] = None  # temperature (should be Celsius)
        self.end_temp: Optional[float] = None  # temperature (should be Celsius)
        self.step_time: Optional[float] = None  # time in minutes
        self.decoction_amt: Optional[Text] = None
        self.version: Optional[int] = None

        # pylint: disable=invalid-name, unused-variable
        @property
        def waterRatio(self):
            raise NotImplementedError("waterRation")
            # water_amout = self.infuse_amount or self.decoction_amt
            # return water_amount / recipe.grainWeight()
