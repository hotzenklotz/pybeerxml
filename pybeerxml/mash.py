from typing import Optional, Text, List
from pybeerxml.mash_step import MashStep


class Mash:
    def __init__(self):
        self.name: Optional[Text] = None
        self.grain_temp: Optional[float] = None
        self.sparge_temp: Optional[float] = None
        # pylint: disable=invalid-name
        self.ph: Optional[float] = None
        self.notes: Optional[Text] = None

        self.steps: List[MashStep] = []
