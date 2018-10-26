class Misc(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.amount = None
        self._amount_is_weight = None
        self.use = None
        self.use_for = None
        self.time = None
        self.notes = None

    @property
    def amount_is_weight(self):
        if isinstance(self._amount_is_weight, str):
            return self._amount_is_weight.lower() == "true"
        elif isinstance(self._amount_is_weight, int) or isinstance(self._amount_is_weight, float):
            return bool(self._amount_is_weight)
        else:
            return False

    @amount_is_weight.setter
    def amount_is_weight(self, value):
        self._amount_is_weight = value
