import math
from typing import Optional, Text


class Hop:
    def __init__(self):
        self.name: Optional[Text] = None
        self.alpha: Optional[float] = None
        self.amount: Optional[float] = None
        self.use: Optional[Text] = None
        self.form: Optional[Text] = None
        self.notes: Optional[Text] = None
        self.time: Optional[float] = None
        self.version: Optional[int] = None
        self.type: Optional[Text] = None
        self.beta: Optional[float] = None
        self.hsi: Optional[float] = None
        self.origin: Optional[Text] = None
        self.substitutes: Optional[Text] = None
        self.humulene: Optional[float] = None
        self.caryophyllene: Optional[float] = None
        self.cohumulone: Optional[float] = None
        self.myrcene: Optional[float] = None

    def utilization_factor(self):
        "Account for better utilization from pellets vs. whole"
        return 1.15 if self.form == "pellet" else 1.0

    def bitterness(self, ibu_method, early_og, batch_size):
        "Calculate bitterness based on chosen method"

        if ibu_method == "tinseth":
            bitterness = (
                1.65
                * math.pow(0.000125, early_og - 1.0)
                * ((1 - math.pow(math.e, -0.04 * self.time)) / 4.15)
                * ((self.alpha / 100.0 * self.amount * 1000000) / batch_size)
                * self.utilization_factor()
            )

        elif ibu_method == "rager":
            utilization = 18.11 + 13.86 * math.tanh((self.time - 31.32) / 18.27)
            adjustment = max(0, (early_og - 1.050) / 0.2)
            bitterness = (
                self.amount
                * 100
                * utilization
                * self.utilization_factor()
                * self.alpha
                / (batch_size * (1 + adjustment))
            )

        else:
            raise Exception("Unknown IBU method %s!" % ibu_method)

        return bitterness
