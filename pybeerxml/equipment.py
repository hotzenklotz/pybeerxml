from pybeerxml.util import cast_to_bool


class Equipment(object):
    def __init__(self):
        self.name = None
        self.version = None
        self.boil_size = None
        self.batch_size = None
        self.tun_volume = None
        self.tun_weight = None
        self.tun_specific_heat = None
        self.top_up_water = None
        self.trub_chiller_loss = None
        self.evap_rate = None
        self.boil_time = None
        self._calc_boil_volume = None
        self.lauter_deadspace = None
        self.top_up_kettle = None
        self.hop_utilization = None
        self.notes = None

    @property
    def calc_boil_volume(self):
        return cast_to_bool(self._calc_boil_volume)

    @calc_boil_volume.setter
    def calc_boil_volume(self, value):
        self._calc_boil_volume = value
