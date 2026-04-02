from dataclasses import dataclass


@dataclass
class Water:
    name: str | None = None
    version: float | None = None
    amount: float | None = None
    calcium: float | None = None
    bicarbonate: float | None = None
    sulfate: float | None = None
    chloride: float | None = None
    sodium: float | None = None
    magnesium: float | None = None
    ph: float | None = None
    notes: str | None = None
    volume: float | None = None
