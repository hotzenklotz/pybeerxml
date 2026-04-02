from dataclasses import dataclass


@dataclass
class Style:
    name: str | None = None
    category: str | None = None
    og_min: float | None = None
    og_max: float | None = None
    fg_min: float | None = None
    fg_max: float | None = None
    ibu_min: float | None = None
    ibu_max: float | None = None
    color_min: float | None = None
    color_max: float | None = None
    abv_min: float | None = None
    abv_max: float | None = None
    carb_min: float | None = None
    carb_max: float | None = None
    notes: str | None = None
