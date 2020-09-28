from typing import Optional, Text


class Water:
    def __init__(self):
        self.name: Optional[Text] = None
        self.version: Optional[float] = None
        self.amount: Optional[float] = None
        self.calcium: Optional[float] = None
        self.bicarbonate: Optional[float] = None
        self.sulfate: Optional[float] = None
        self.chloride: Optional[float] = None
        self.sodium: Optional[float] = None
        self.magnesium: Optional[float] = None
        # pylint: disable=invalid-name
        self.ph: Optional[float] = None
        self.notes: Optional[Text] = None
        self.volume: Optional[float] = None
