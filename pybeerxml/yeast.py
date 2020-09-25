from typing import Optional, Text


class Yeast:
    def __init__(self):
        self.name: Optional[Text] = None
        self.type: Optional[Text] = None
        self.form: Optional[Text] = None  # May be "Liquid", "Dry", "Slant" or "Culture"
        self.attenuation: Optional[float] = None  # Percent
        self.notes: Optional[Text] = None
        self.laboratory: Optional[Text] = None
        self.product_id: Optional[Text] = None
        self.flocculation: Optional[
            Text
        ] = None  # May be "Low", "Medium", "High" or "Very High"
