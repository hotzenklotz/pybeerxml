from typing import Optional, Text


class Style:
    def __init__(self):
        self.name: Optional[Text] = None
        self.category: Optional[Text] = None
        self.og_min: Optional[float] = None
        self.og_max: Optional[float] = None
        self.fg_min: Optional[float] = None
        self.fg_max: Optional[float] = None
        self.ibu_min: Optional[float] = None
        self.ibu_max: Optional[float] = None
        self.color_min: Optional[float] = None
        self.color_max: Optional[float] = None
        self.abv_min: Optional[float] = None
        self.abv_max: Optional[float] = None
        self.carb_min: Optional[float] = None
        self.carb_max: Optional[float] = None
        self.notes: Optional[Text] = None
