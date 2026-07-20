import logging

from pydantic_xml import element, wrapped

from pybeerxml.base import BeerXmlModel, LenientFloat
from pybeerxml.equipment import Equipment
from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.misc import Misc
from pybeerxml.style import Style
from pybeerxml.utils import gravity_to_plato
from pybeerxml.water import Water
from pybeerxml.yeast import Yeast

logger = logging.getLogger(__name__)


class Recipe(BeerXmlModel, tag="RECIPE"):
    """A complete beer recipe parsed from a BeerXML document.

    Scalar fields (``name``, ``batch_size``, etc.) are populated directly from
    the XML.  The five key brewing metrics — OG, FG, IBU, ABV, and colour —
    expose both the stored XML value and an independently calculated value:

    - The plain property (e.g. ``recipe.og``) returns the stored XML value when
      present and falls back to the calculated value automatically.
    - The trailing-underscore field (e.g. ``recipe.og_``) holds exactly the
      value stored in the XML (``<OG>``), or ``None`` when absent. Only these
      stored fields are written back during serialization.
    - The ``_calculated`` variant (e.g. ``recipe.og_calculated``) always
      computes from the ingredient list, regardless of what the XML says.

    The previous private attribute names (``_og``, ``_fg``, ``_ibu``, ``_abv``,
    ``_color``) remain available as compatibility aliases for ``og_``, ``fg_``,
    ``ibu_``, ``abv_``, and ``color_``.

    All gravity values are also available in degrees Plato via ``og_plato``,
    ``og_calculated_plato``, ``fg_plato``, and ``fg_calculated_plato``.

    Attributes:
        name: Recipe name.
        brewer: Brewer's name.
        type: Recipe type, e.g. ``"All Grain"`` or ``"Extract"``.
        batch_size: Target batch volume in litres.
        boil_size: Pre-boil volume in litres.
        boil_time: Boil duration in minutes.
        efficiency: Mash efficiency as a percentage.
        notes: Free-text recipe notes.
        date: Recipe creation date (stored as a string, e.g. ``"3 Dec 04"``).
        hops: Hop additions.
        fermentables: Fermentable ingredients.
        yeasts: Yeast strains.
        miscs: Miscellaneous ingredients.
        waters: Water chemistry profiles.
        mash: Mash profile and steps.
        style: Beer style guidelines.
        equipment: Equipment profile.

    Examples:
        >>> from pybeerxml import Parser
        >>> recipe = Parser().parse("recipe.beerxml")[0]
        >>> print(recipe.name, round(recipe.og, 4), round(recipe.ibu, 1))
        Simcoe IPA 1.0756 64.3
    """

    name: str | None = element(tag="NAME", default=None)
    version: int | None = element(tag="VERSION", default=None)
    type: str | None = element(tag="TYPE", default=None)
    brewer: str | None = element(tag="BREWER", default=None)
    asst_brewer: str | None = element(tag="ASST_BREWER", default=None)
    batch_size: float | None = element(tag="BATCH_SIZE", default=None)
    boil_time: LenientFloat = element(tag="BOIL_TIME", default=None)
    boil_size: LenientFloat = element(tag="BOIL_SIZE", default=None)
    efficiency: LenientFloat = element(tag="EFFICIENCY", default=None)
    notes: str | None = element(tag="NOTES", default=None)
    taste_notes: str | None = element(tag="TASTE_NOTES", default=None)
    taste_rating: LenientFloat = element(tag="TASTE_RATING", default=None)
    fermentation_stages: int | None = element(tag="FERMENTATION_STAGES", default=None)
    primary_age: LenientFloat = element(tag="PRIMARY_AGE", default=None)
    primary_temp: LenientFloat = element(tag="PRIMARY_TEMP", default=None)
    secondary_age: LenientFloat = element(tag="SECONDARY_AGE", default=None)
    secondary_temp: LenientFloat = element(tag="SECONDARY_TEMP", default=None)
    tertiary_age: LenientFloat = element(tag="TERTIARY_AGE", default=None)
    tertiary_temp: LenientFloat = element(tag="TERTIARY_TEMP", default=None)
    carbonation: LenientFloat = element(tag="CARBONATION", default=None)
    carbonation_temp: LenientFloat = element(tag="CARBONATION_TEMP", default=None)
    age: LenientFloat = element(tag="AGE", default=None)
    age_temp: LenientFloat = element(tag="AGE_TEMP", default=None)
    date: str | None = element(tag="DATE", default=None)
    forced_carbonation: bool | None = element(tag="FORCED_CARBONATION", default=None)
    priming_sugar_name: str | None = element(tag="PRIMING_SUGAR_NAME", default=None)
    priming_sugar_equiv: LenientFloat = element(tag="PRIMING_SUGAR_EQUIV", default=None)
    keg_priming_factor: LenientFloat = element(tag="KEG_PRIMING_FACTOR", default=None)

    # Values stored in the XML; the matching public properties fall back to
    # calculated values when these are None. Only these fields serialize.
    og_: LenientFloat = element(tag="OG", default=None)
    fg_: LenientFloat = element(tag="FG", default=None)
    ibu_: LenientFloat = element(tag="IBU", default=None)
    abv_: LenientFloat = element(tag="ABV", default=None)
    color_: LenientFloat = element(tag="COLOR", default=None)

    # Recipe extension fields
    est_og: LenientFloat = element(tag="EST_OG", default=None)
    est_fg: LenientFloat = element(tag="EST_FG", default=None)
    est_color: LenientFloat = element(tag="EST_COLOR", default=None)
    ibu_method: str | None = element(tag="IBU_METHOD", default=None)
    est_abv: LenientFloat = element(tag="EST_ABV", default=None)
    actual_efficiency: LenientFloat = element(tag="ACTUAL_EFFICIENCY", default=None)
    calories: str | None = element(tag="CALORIES", default=None)
    carbonation_used: str | None = element(tag="CARBONATION_USED", default=None)

    style: Style | None = element(tag="STYLE", default=None)
    equipment: Equipment | None = element(tag="EQUIPMENT", default=None)
    mash: Mash | None = element(tag="MASH", default=None)
    hops: list[Hop] = wrapped("HOPS", element(tag="HOP"), default_factory=list)
    fermentables: list[Fermentable] = wrapped("FERMENTABLES", element(tag="FERMENTABLE"), default_factory=list)
    yeasts: list[Yeast] = wrapped("YEASTS", element(tag="YEAST"), default_factory=list)
    miscs: list[Misc] = wrapped("MISCS", element(tag="MISC"), default_factory=list)
    waters: list[Water] = wrapped("WATERS", element(tag="WATER"), default_factory=list)

    @property
    def _og(self) -> float | str | None:
        """Compatibility alias for `og_`."""
        return self.og_

    @_og.setter
    def _og(self, value: float | str | None) -> None:
        self.og_ = value

    @property
    def _fg(self) -> float | str | None:
        """Compatibility alias for `fg_`."""
        return self.fg_

    @_fg.setter
    def _fg(self, value: float | str | None) -> None:
        self.fg_ = value

    @property
    def _ibu(self) -> float | str | None:
        """Compatibility alias for `ibu_`."""
        return self.ibu_

    @_ibu.setter
    def _ibu(self, value: float | str | None) -> None:
        self.ibu_ = value

    @property
    def _abv(self) -> float | str | None:
        """Compatibility alias for `abv_`."""
        return self.abv_

    @_abv.setter
    def _abv(self, value: float | str | None) -> None:
        self.abv_ = value

    @property
    def _color(self) -> float | str | None:
        """Compatibility alias for `color_`."""
        return self.color_

    @_color.setter
    def _color(self, value: float | str | None) -> None:
        self.color_ = value

    @property
    def _forced_carbonation(self) -> bool | None:
        """Compatibility alias for `forced_carbonation`."""
        return self.forced_carbonation

    @_forced_carbonation.setter
    def _forced_carbonation(self, value: bool | None) -> None:
        self.forced_carbonation = value

    @property
    def abv(self):
        """ABV in percent.

        Returns the value stored in the XML when available, otherwise falls
        back to `abv_calculated`.
        """
        if self.abv_ is not None:
            return self.abv_
        logger.debug("The value for ABV has been calculated from OG and FG")
        return self.abv_calculated

    @abv.setter
    def abv(self, value):
        self.abv_ = value

    @property
    def abv_calculated(self):
        """ABV in percent, always computed from `og_calculated` and `fg_calculated`."""
        return ((1.05 * (self.og_calculated - self.fg_calculated)) / self.fg_calculated) / 0.79 * 100.0

    @property
    def og_plato(self):
        """`og` expressed in degrees Plato."""
        return gravity_to_plato(self.og)

    @property
    def og_calculated_plato(self):
        """`og_calculated` expressed in degrees Plato."""
        return gravity_to_plato(self.og_calculated)

    @property
    def fg_plato(self):
        """`fg` expressed in degrees Plato."""
        return gravity_to_plato(self.fg)

    @property
    def fg_calculated_plato(self):
        """`fg_calculated` expressed in degrees Plato."""
        return gravity_to_plato(self.fg_calculated)

    @property
    def ibu(self):
        """IBU bitterness.

        Returns the value stored in the XML when available, otherwise falls
        back to `ibu_calculated`.
        """
        if self.ibu_ is not None:
            return self.ibu_
        logger.debug("The value for IBU has been calculated from the hop bill using Tinseth's formula")
        return self.ibu_calculated

    @ibu.setter
    def ibu(self, value):
        self.ibu_ = value

    @property
    def ibu_calculated(self):
        """IBU, always computed from boil hops using the Tinseth formula.

        Only hops with ``use == "boil"`` contribute. Returns ``0.0`` when
        ``batch_size`` is not set.
        """
        if self.batch_size is None:
            return 0.0
        ibu_method = "tinseth"
        _ibu = 0.0
        for hop in self.hops:
            if hop.alpha and hop.use is not None and hop.use.lower() == "boil":
                _ibu += hop.bitterness(ibu_method, self.og_calculated, self.batch_size)
        return _ibu

    @property
    def og(self):
        """Original gravity in SG.

        Returns the value stored in the XML when available, otherwise falls
        back to `og_calculated`.
        """
        if self.og_ is not None:
            return self.og_
        logger.debug("The value for OG has been calculated from the mashing steps")
        return self.og_calculated

    @og.setter
    def og(self, value):
        self.og_ = value

    @property
    def og_calculated(self):
        """Original gravity in SG, always computed from the fermentable bill.

        Uses fixed efficiencies: **50 %** for steep additions, **75 %** for
        mash additions, and **100 %** for direct additions (extracts, sugars).
        Returns ``1.0`` when ``batch_size`` is not set.
        """
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

    @property
    def fg(self):
        """Final gravity in SG.

        Returns the value stored in the XML when available, otherwise falls
        back to `fg_calculated`.
        """
        if self.fg_ is not None:
            return self.fg_
        logger.debug("The value for FG has been calculated from OG and yeast")
        return self.fg_calculated

    @fg.setter
    def fg(self, value):
        self.fg_ = value

    @property
    def fg_calculated(self):
        """Final gravity in SG, always computed from `og_calculated` and yeast attenuation.

        Uses the highest attenuation value among all yeasts. Defaults to
        **75 %** attenuation when no yeast is present.
        """
        attenuation = 0.0
        for yeast in self.yeasts:
            if yeast.attenuation is not None and yeast.attenuation > attenuation:
                attenuation = yeast.attenuation
        if attenuation == 0:
            attenuation = 75.0
        return self.og_calculated - ((self.og_calculated - 1.0) * attenuation / 100.0)

    @property
    def color(self):
        """Beer colour in SRM.

        Returns the value stored in the XML when available, otherwise falls
        back to `color_calculated`.
        """
        if self.color_ is not None:
            return self.color_
        logger.debug("The value for color has been calculated from fermentables using the Morey Equation")
        return self.color_calculated

    @color.setter
    def color(self, value):
        self.color_ = value

    @property
    def color_calculated(self):
        """Beer colour in SRM, always computed using the Morey equation.

        Returns ``0.0`` when ``batch_size`` is not set.
        """
        if self.batch_size is None:
            return 0.0
        mcu = 0.0
        for fermentable in self.fermentables:
            if fermentable.amount is not None and fermentable.color is not None:
                # 8.3454 is conversion factor from kg/L to lb/gal
                mcu += fermentable.amount * fermentable.color * 8.3454 / self.batch_size
        return 1.4922 * (mcu**0.6859)


class Recipes(BeerXmlModel, tag="RECIPES"):
    """Root element of a BeerXML document, containing one or more recipes.

    Used internally by `pybeerxml.Parser` and `pybeerxml.Serializer` to read
    and write the ``<RECIPES>`` document wrapper.

    Attributes:
        recipes: The recipes contained in the document.
    """

    recipes: list[Recipe] = element(tag="RECIPE", default_factory=list)
