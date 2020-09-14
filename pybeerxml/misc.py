from pybeerxml.util import cast_to_bool


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
        return cast_to_bool(self._amount_is_weight)

    @amount_is_weight.setter
    def amount_is_weight(self, value):
        self._amount_is_weight = value
