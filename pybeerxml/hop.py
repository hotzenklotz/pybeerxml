import math


class Hop:
    def __init__(self):
        self.name: str | None = None
        self.alpha: float | None = None
        self.amount: float | None = None
        self.use: str | None = None
        self.form: str | None = None
        self.notes: str | None = None
        self.time: float | None = None
        self.version: int | None = None
        self.type: str | None = None
        self.beta: float | None = None
        self.hsi: float | None = None
        self.origin: str | None = None
        self.substitutes: str | None = None
        self.humulene: float | None = None
        self.caryophyllene: float | None = None
        self.cohumulone: float | None = None
        self.myrcene: float | None = None

    def utilization_factor(self) -> float:
        "Account for better utilization from pellets vs. whole"
        return 1.15 if self.form == "pellet" else 1.0

    def bitterness(self, ibu_method: str, early_og: float, batch_size: float) -> float:
        "Calculate bitterness based on chosen method"

        if self.time is None or self.alpha is None or self.amount is None:
            raise ValueError("Hop is missing required fields (time, alpha, amount) for bitterness calculation")

        if ibu_method == "tinseth":
            return (
                1.65
                * math.pow(0.000125, early_og - 1.0)
                * ((1 - math.pow(math.e, -0.04 * self.time)) / 4.15)
                * ((self.alpha / 100.0 * self.amount * 1000000) / batch_size)
                * self.utilization_factor()
            )

        if ibu_method == "rager":
            utilization = 18.11 + 13.86 * math.tanh((self.time - 31.32) / 18.27)
            adjustment = max(0, (early_og - 1.050) / 0.2)
            return (
                self.amount
                * 100
                * utilization
                * self.utilization_factor()
                * self.alpha
                / (batch_size * (1 + adjustment))
            )

        raise ValueError(f"Unknown IBU method: {ibu_method!r}")
