from typing import Optional, Text, List, Any

from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.misc import Misc
from pybeerxml.yeast import Yeast
from pybeerxml.style import Style
from pybeerxml.water import Water
from pybeerxml.equipment import Equipment
from pybeerxml.utils import cast_to_bool

# pylint: disable=too-many-instance-attributes
class Recipe:
    def __init__(self):
        self.name: Optional[Text] = None
        self.version: Optional[float] = None
        self.type: Optional[Text] = None
        self.brewer: Optional[Text] = None
        self.asst_brewer: Optional[Text] = None
        self.batch_size: Optional[float] = None
        self.boil_time: Optional[float] = None
        self.boil_size: Optional[float] = None
        self.efficiency: Optional[float] = None
        self.notes: Optional[Text] = None
        self.taste_notes: Optional[Text] = None
        self.taste_rating: Optional[float] = None
        self.fermentation_stages: Optional[Text] = None
        self.primary_age: Optional[float] = None
        self.primary_temp: Optional[float] = None
        self.secondary_age: Optional[float] = None
        self.secondary_temp: Optional[float] = None
        self.tertiary_age: Optional[float] = None
        self.tertiary_temp: Optional[float] = None
        self.carbonation: Optional[float] = None
        self.carbonation_temp: Optional[float] = None
        self.age: Optional[float] = None
        self.age_temp: Optional[float] = None
        self.date: Optional[float] = None
        self.carbonation: Optional[float] = None
        self._forced_carbonation: Optional[bool] = None
        self.priming_sugar_name: Optional[float] = None
        self.carbonation_temp: Optional[float] = None
        self.priming_sugar_equiv: Optional[Text] = None
        self.keg_priming_factor: Optional[float] = None

        # Recipe extension fields
        self.est_og = None
        self.est_fg = None
        self.est_color = None
        self.ibu_method = None
        self.est_abv = None
        self.actual_efficiency = None
        self.calories = None
        self.carbonation_used = None

        self.style: Optional[Style] = None
        self.hops: List[Hop] = []
        self.yeasts: List[Yeast] = []
        self.fermentables: List[Fermentable] = []
        self.miscs: List[Misc] = []
        self.mash: Optional[Mash] = None
        self.waters: List[Water] = []
        self.equipment: Optional[Equipment] = None

    @property
    def abv(self):
        return ((1.05 * (self.og - self.fg)) / self.fg) / 0.79 * 100.0

    @abv.setter
    def set_abv(self, value):
        pass

    # Gravity degrees plato approximations
    @property
    def og_plato(self):
        og = self.og
        return (-463.37) + (668.72 * og) - (205.35 * (og * og))

    @property
    def fg_plato(self):
        fg = self.fg
        return (-463.37) + (668.72 * fg) - (205.35 * (fg * fg))

    @property
    def ibu(self):

        ibu_method = "tinseth"
        _ibu = 0.0

        for hop in self.hops:
            if hop.alpha and hop.use.lower() == "boil":
                _ibu += hop.bitterness(ibu_method, self.og, self.batch_size)

        return _ibu

    @ibu.setter
    def set_ibu(self, value):
        pass

    # pylint: disable=invalid-name
    @property
    def og(self):

        _og = 1.0
        steep_efficiency = 50
        mash_efficiency = 75

        # Calculate gravities and color from fermentables
        for fermentable in self.fermentables:
            addition = fermentable.addition
            if addition == "steep":
                efficiency = steep_efficiency / 100.0
            elif addition == "mash":
                efficiency = mash_efficiency / 100.0
            else:
                efficiency = 1.0

            # Update gravities
            gu = fermentable.gu(self.batch_size) * efficiency
            gravity = gu / 1000.0
            _og += gravity

        return _og

    @og.setter
    def set_og(self, value):
        pass

    # pylint: disable=invalid-name
    @property
    def fg(self):

        _fg = 0
        attenuation = 0

        # Get attenuation for final gravity
        for yeast in self.yeasts:
            if yeast.attenuation > attenuation:
                attenuation = yeast.attenuation

        if attenuation == 0:
            attenuation = 75.0

        _fg = self.og - ((self.og - 1.0) * attenuation / 100.0)

        return _fg

    @fg.setter
    def set_fg(self, value):
        pass

    @property
    def color(self):
        # Formula source: http://brewwiki.com/index.php/Estimating_Color
        mcu = 0.0
        for fermentable in self.fermentables:
            if fermentable.amount is not None and fermentable.color is not None:
                # 8.3454 is conversion factor from kg/L to lb/gal
                mcu += fermentable.amount * fermentable.color * 8.3454 / self.batch_size
        return 1.4922 * (mcu ** 0.6859)

    @color.setter
    def set_color(self, value):
        pass

    @property
    def forced_carbonation(self):
        return self._forced_carbonation

    @forced_carbonation.setter
    def forced_carbonation(self, value: Any) -> bool:
        self._forced_carbonation = cast_to_bool(value)
