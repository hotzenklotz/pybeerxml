from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.recipe import Recipe
from pybeerxml.yeast import Yeast


class TestPropertyOverrides:
    """XML-provided values should take precedence over calculated values."""

    def test_og_override(self):
        recipe = Recipe()
        recipe.og = 1.10
        assert recipe.og == 1.10
        assert recipe.og_calculated == 1.0  # no fermentables

    def test_fg_override(self):
        recipe = Recipe()
        recipe.fg = 1.02
        assert recipe.fg == 1.02

    def test_ibu_override(self):
        recipe = Recipe()
        recipe.ibu = 40.0
        assert recipe.ibu == 40.0

    def test_abv_override(self):
        recipe = Recipe()
        recipe.abv = 5.5
        assert recipe.abv == 5.5

    def test_color_override(self):
        recipe = Recipe()
        recipe.color = 12.0
        assert recipe.color == 12.0


class TestOgCalculated:
    def test_no_fermentables(self):
        recipe = Recipe()
        recipe.batch_size = 20.0
        assert recipe.og_calculated == 1.0

    def test_none_batch_size_returns_base(self):
        recipe = Recipe()
        assert recipe.og_calculated == 1.0

    def test_increases_with_fermentables(self):
        recipe = Recipe()
        recipe.batch_size = 20.0
        f = Fermentable()
        f.name = "Pale Malt"
        f._yield = 80
        f.amount = 5
        recipe.fermentables.append(f)
        assert recipe.og_calculated > 1.0


class TestIbuCalculated:
    def test_none_batch_size_returns_zero(self):
        recipe = Recipe()
        h = Hop()
        h.time = 60
        h.alpha = 10
        h.amount = 0.010
        h.use = "boil"
        recipe.hops.append(h)
        assert recipe.ibu_calculated == 0.0

    def test_non_boil_hops_excluded(self):
        recipe = Recipe()
        recipe.batch_size = 20.0
        for use in ("dry hop", "aroma", "whirlpool"):
            h = Hop()
            h.time = 10
            h.alpha = 10
            h.amount = 0.010
            h.use = use
            recipe.hops.append(h)
        assert recipe.ibu_calculated == 0.0

    def test_boil_hops_contribute(self):
        recipe = Recipe()
        recipe.batch_size = 20.0
        h = Hop()
        h.time = 60
        h.alpha = 10
        h.amount = 0.010
        h.use = "boil"
        recipe.hops.append(h)
        assert recipe.ibu_calculated > 0.0


class TestFgCalculated:
    def test_no_yeasts_uses_default_attenuation(self):
        # Default attenuation is 75%
        recipe = Recipe()
        recipe.batch_size = 20.0
        og = recipe.og_calculated  # 1.0 with no fermentables
        fg = recipe.fg_calculated
        assert fg == og - ((og - 1.0) * 0.75)

    def test_uses_highest_attenuation_yeast(self):
        recipe = Recipe()
        y1 = Yeast()
        y1.attenuation = 70.0
        y2 = Yeast()
        y2.attenuation = 80.0
        recipe.yeasts.extend([y1, y2])
        og = recipe.og_calculated
        expected_fg = og - ((og - 1.0) * 0.80)
        assert recipe.fg_calculated == expected_fg


class TestColorCalculated:
    def test_none_batch_size_returns_zero(self):
        recipe = Recipe()
        f = Fermentable()
        f.amount = 5.0
        f.color = 10.0
        recipe.fermentables.append(f)
        assert recipe.color_calculated == 0.0

    def test_no_fermentables_returns_zero(self):
        recipe = Recipe()
        recipe.batch_size = 20.0
        assert recipe.color_calculated == 0.0

    def test_increases_with_darker_malts(self):
        recipe = Recipe()
        recipe.batch_size = 20.0

        f_pale = Fermentable()
        f_pale.amount = 5.0
        f_pale.color = 3.0

        f_dark = Fermentable()
        f_dark.amount = 5.0
        f_dark.color = 500.0

        recipe.fermentables.append(f_pale)
        light = recipe.color_calculated

        recipe.fermentables.append(f_dark)
        dark = recipe.color_calculated

        assert dark > light


class TestForcedCarbonation:
    def test_string_true(self):
        recipe = Recipe()
        recipe.forced_carbonation = "TRUE"
        assert recipe.forced_carbonation is True

    def test_string_false(self):
        recipe = Recipe()
        recipe.forced_carbonation = "false"
        assert recipe.forced_carbonation is False

    def test_default_is_none(self):
        assert Recipe().forced_carbonation is None


class TestInstanceIndependence:
    """Two Recipe instances must not share mutable list state."""

    def test_hops_are_independent(self):
        r1, r2 = Recipe(), Recipe()
        r1.hops.append(Hop())
        assert len(r2.hops) == 0

    def test_fermentables_are_independent(self):
        r1, r2 = Recipe(), Recipe()
        r1.fermentables.append(Fermentable())
        assert len(r2.fermentables) == 0

    def test_yeasts_are_independent(self):
        r1, r2 = Recipe(), Recipe()
        r1.yeasts.append(Yeast())
        assert len(r2.yeasts) == 0
