import logging
from typing import Any

from pybeerxml.equipment import Equipment
from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.misc import Misc
from pybeerxml.style import Style
from pybeerxml.utils import cast_to_bool, gravity_to_plato
from pybeerxml.water import Water
from pybeerxml.yeast import Yeast

logger = logging.getLogger(__name__)


class Recipe:
    def __init__(self):
        self.name: str | None = None
        self.version: float | None = None
        self.type: str | None = None
        self.brewer: str | None = None
        self.asst_brewer: str | None = None
        self.batch_size: float | None = None
        self.boil_time: float | None = None
        self.boil_size: float | None = None
        self.efficiency: float | None = None
        self.notes: str | None = None
        self.taste_notes: str | None = None
        self.taste_rating: float | None = None
        self.fermentation_stages: int | None = None
        self.primary_age: float | None = None
        self.primary_temp: float | None = None
        self.secondary_age: float | None = None
        self.secondary_temp: float | None = None
        self.tertiary_age: float | None = None
        self.tertiary_temp: float | None = None
        self.carbonation: float | None = None
        self.carbonation_temp: float | None = None
        self.age: float | None = None
        self.age_temp: float | None = None
        self.date: str | None = None
        self._forced_carbonation: bool | None = None
        self.priming_sugar_name: str | None = None
        self.priming_sugar_equiv: float | None = None
        self.keg_priming_factor: float | None = None

        # Recipe extension fields
        self.est_og: float | None = None
        self.est_fg: float | None = None
        self.est_color: float | None = None
        self.ibu_method: str | None = None
        self.est_abv: float | None = None
        self.actual_efficiency: float | None = None
        self.calories: str | None = None
        self.carbonation_used: str | None = None

        # Values from the recipe, which are calculated as a fallback
        self._abv: float | None = None
        self._og: float | None = None
        self._fg: float | None = None
        self._ibu: float | None = None
        self._color: float | None = None

        self.style: Style | None = None
        self.hops: list[Hop] = []
        self.yeasts: list[Yeast] = []
        self.fermentables: list[Fermentable] = []
        self.miscs: list[Misc] = []
        self.mash: Mash | None = None
        self.waters: list[Water] = []
        self.equipment: Equipment | None = None

    @property
    def abv(self):
        if self._abv is not None:
            return self._abv
        logger.debug("The value for ABV has been calculated from OG and FG")
        return self.abv_calculated

    @abv.setter
    def abv(self, value):
        self._abv = value

    @property
    def abv_calculated(self):
        return ((1.05 * (self.og_calculated - self.fg_calculated)) / self.fg_calculated) / 0.79 * 100.0

    @abv_calculated.setter
    def abv_calculated(self, value):
        pass

    # Gravity degrees plato approximations
    @property
    def og_plato(self):
        return gravity_to_plato(self.og)

    @og_plato.setter
    def og_plato(self, value):
        pass

    @property
    def og_calculated_plato(self):
        return gravity_to_plato(self.og_calculated)

    @og_calculated_plato.setter
    def og_calculated_plato(self, value):
        pass

    @property
    def fg_plato(self):
        return gravity_to_plato(self.fg)

    @fg_plato.setter
    def fg_plato(self, value):
        pass

    @property
    def fg_calculated_plato(self):
        return gravity_to_plato(self.fg_calculated)

    @fg_calculated_plato.setter
    def fg_calculated_plato(self, value):
        pass

    @property
    def ibu(self):
        if self._ibu is not None:
            return self._ibu
        logger.debug("The value for IBU has been calculated from the hop bill using Tinseth's formula")
        return self.ibu_calculated

    @ibu.setter
    def ibu(self, value):
        self._ibu = value

    @property
    def ibu_calculated(self):
        if self.batch_size is None:
            return 0.0
        ibu_method = "tinseth"
        _ibu = 0.0
        for hop in self.hops:
            if hop.alpha and hop.use is not None and hop.use.lower() == "boil":
                _ibu += hop.bitterness(ibu_method, self.og_calculated, self.batch_size)
        return _ibu

    @ibu_calculated.setter
    def ibu_calculated(self, value):
        pass

    @property
    def og(self):
        if self._og is not None:
            return self._og
        logger.debug("The value for OG has been calculated from the mashing steps")
        return self.og_calculated

    @og.setter
    def og(self, value):
        self._og = value

    @property
    def og_calculated(self):
        _og = 1.0
        steep_efficiency = 50
        mash_efficiency = 75

        if self.batch_size is None:
            return _og

        for fermentable in self.fermentables:
            addition = fermentable.addition
            if addition == "steep":
                efficiency = steep_efficiency / 100.0
            elif addition == "mash":
                efficiency = mash_efficiency / 100.0
            else:
                efficiency = 1.0

            gu = fermentable.gu(self.batch_size)
            if gu is None:
                continue
            _og += gu * efficiency / 1000.0

        return _og

    @og_calculated.setter
    def og_calculated(self, value):
        pass

    @property
    def fg(self):
        if self._fg is not None:
            return self._fg
        logger.debug("The value for FG has been calculated from OG and yeast")
        return self.fg_calculated

    @fg.setter
    def fg(self, value):
        self._fg = value

    @property
    def fg_calculated(self):
        attenuation = 0.0
        for yeast in self.yeasts:
            if yeast.attenuation is not None and yeast.attenuation > attenuation:
                attenuation = yeast.attenuation
        if attenuation == 0:
            attenuation = 75.0
        return self.og_calculated - ((self.og_calculated - 1.0) * attenuation / 100.0)

    @fg_calculated.setter
    def fg_calculated(self, value):
        pass

    @property
    def color(self):
        if self._color is not None:
            return self._color
        logger.debug("The value for color has been calculated from fermentables using the Morey Equation")
        return self.color_calculated

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def color_calculated(self):
        # Formula source: http://brewwiki.com/index.php/Estimating_Color
        if self.batch_size is None:
            return 0.0
        mcu = 0.0
        for fermentable in self.fermentables:
            if fermentable.amount is not None and fermentable.color is not None:
                # 8.3454 is conversion factor from kg/L to lb/gal
                mcu += fermentable.amount * fermentable.color * 8.3454 / self.batch_size
        return 1.4922 * (mcu**0.6859)

    @color_calculated.setter
    def color_calculated(self, value):
        pass

    @property
    def forced_carbonation(self):
        return self._forced_carbonation

    @forced_carbonation.setter
    def forced_carbonation(self, value: Any):
        self._forced_carbonation = cast_to_bool(value)
