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
        return bool(self._amount_is_weight)

    @amount_is_weight.setter
    def amount_is_weight(self, value):
        print(value)
        self._amount_is_weight = value
