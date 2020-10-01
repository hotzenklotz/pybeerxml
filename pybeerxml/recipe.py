import logging
from typing import Optional, Text, List, Any

from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.misc import Misc
from pybeerxml.yeast import Yeast
from pybeerxml.style import Style
from pybeerxml.water import Water
from pybeerxml.equipment import Equipment
from pybeerxml.utils import cast_to_bool, gravity_to_plato

logger = logging.getLogger(__name__)

# pylint: disable=too-many-instance-attributes, too-many-statements, too-many-public-methods
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
        self.est_og: Optional[float] = None
        self.est_fg: Optional[float] = None
        self.est_color: Optional[float] = None
        self.ibu_method: Optional[Text] = None
        self.est_abv: Optional[float] = None
        self.actual_efficiency: Optional[float] = None
        self.calories: Optional[float] = None
        self.carbonation_used: Optional[Text] = None

        # Values from the recipe, which are calculated as a fallback
        self._abv = None
        self._og = None
        self._fg = None
        self._ibu = None
        self._color = None

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

        if self._abv is not None:
            return self._abv

        logger.debug("The value for ABV has been calculated from OG and FG")
        return self.abv_calculated

    @abv.setter
    def abv(self, value):
        self._abv = value

    @property
    def abv_calculated(self):
        return (
            ((1.05 * (self.og_calculated - self.fg_calculated)) / self.fg_calculated)
            / 0.79
            * 100.0
        )

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

        logger.debug(
            "The value for IBU has been calculated from the hop bill using Tinseth's formula"
        )
        return self.ibu_calculated

    @ibu.setter
    def ibu(self, value):
        self._ibu = value

    @property
    def ibu_calculated(self):

        ibu_method = "tinseth"
        _ibu = 0.0

        for hop in self.hops:
            if hop.alpha and hop.use.lower() == "boil":
                _ibu += hop.bitterness(ibu_method, self.og_calculated, self.batch_size)

        return _ibu

    @ibu_calculated.setter
    def ibu_calculated(self, value):
        pass

    # pylint: disable=invalid-name
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

    @og_calculated.setter
    def og_calculated(self, value):
        pass

    # pylint: disable=invalid-name
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

        _fg = 0
        attenuation = 0

        # Get attenuation for final gravity
        for yeast in self.yeasts:
            if yeast.attenuation is not None and yeast.attenuation > attenuation:
                attenuation = yeast.attenuation

        if attenuation == 0:
            attenuation = 75.0

        _fg = self.og_calculated - ((self.og_calculated - 1.0) * attenuation / 100.0)

        return _fg

    @fg_calculated.setter
    def fg_calculated(self, value):
        pass

    @property
    def color(self):

        if self._color is not None:
            return self._color

        logger.debug(
            "The value for color has been calculated from fermentables using the Morey Equation"
        )
        return self.color_calculated

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def color_calculated(self):
        # Formula source: http://brewwiki.com/index.php/Estimating_Color
        mcu = 0.0
        for fermentable in self.fermentables:
            if fermentable.amount is not None and fermentable.color is not None:
                # 8.3454 is conversion factor from kg/L to lb/gal
                mcu += fermentable.amount * fermentable.color * 8.3454 / self.batch_size
        return 1.4922 * (mcu ** 0.6859)

    @color_calculated.setter
    def color_calculated(self, value):
        pass

    @property
    def forced_carbonation(self):
        return self._forced_carbonation

    @forced_carbonation.setter
    def forced_carbonation(self, value: Any):
        self._forced_carbonation = cast_to_bool(value)
