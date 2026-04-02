import pytest

from pybeerxml.fermentable import Fermentable


class TestAddAfterBoil:
    def test_set_true(self):
        f = Fermentable()
        f.add_after_boil = True
        assert f.add_after_boil is True

    def test_set_false(self):
        f = Fermentable()
        f.add_after_boil = False
        assert f.add_after_boil is False

    def test_default_is_false(self):
        assert Fermentable().add_after_boil is False

    def test_string_true(self):
        f = Fermentable()
        f.add_after_boil = "TRUE"
        assert f.add_after_boil is True

    def test_string_false(self):
        f = Fermentable()
        f.add_after_boil = "false"
        assert f.add_after_boil is False


class TestPpg:
    def test_calculated(self):
        f = Fermentable()
        f._yield = 1
        assert f.ppg == 0.46214

    def test_none_when_yield_missing(self):
        assert Fermentable().ppg is None


class TestAddition:
    def test_steep_by_ingredient_name(self):
        f = Fermentable()
        f.name = "Munich Malt"
        assert f.addition == "steep"

    def test_boil_by_ingredient_name(self):
        f = Fermentable()
        f.name = "Honey"
        assert f.addition == "boil"

    def test_case_insensitive(self):
        f = Fermentable()
        f.name = "MUNICH MALT"
        assert f.addition == "steep"

        f.name = "HONEY"
        assert f.addition == "boil"

    def test_force_steep_keyword(self):
        f = Fermentable()
        f.name = "Steep Grain"
        assert f.addition == "steep"

    def test_force_boil_keyword(self):
        f = Fermentable()
        f.name = "Boil Sugar"
        assert f.addition == "boil"

    def test_defaults_to_mash(self):
        f = Fermentable()
        f.name = "Pilsner Malt"
        assert f.addition == "mash"

    def test_none_name_defaults_to_mash(self):
        assert Fermentable().addition == "mash"

    @pytest.mark.parametrize(
        "name",
        [
            "Biscuit Malt",
            "Black Malt",
            "Cara Malt",
            "Chocolate Malt",
            "Crystal 60",
            "Munich Malt",
            "Roasted Barley",
            "Special B",
            "Toast Malt",
            "Victory Malt",
            "Vienna Malt",
        ],
    )
    def test_steep_ingredients(self, name):
        f = Fermentable()
        f.name = name
        assert f.addition == "steep", f"{name!r} should be 'steep'"

    @pytest.mark.parametrize(
        "name",
        [
            "Candi Sugar",
            "Candy Sugar",
            "DME",
            "Dry Malt Extract",
            "Honey",
            "LME",
            "Liquid Malt Extract",
            "Table Sugar",
            "Corn Syrup",
            "Turbinado Sugar",
        ],
    )
    def test_boil_ingredients(self, name):
        f = Fermentable()
        f.name = name
        assert f.addition == "boil", f"{name!r} should be 'boil'"


class TestGu:
    def test_calculated(self):
        f = Fermentable()
        f._yield = 1
        f.amount = 1  # kg
        assert f.gu() == 3.8567413912148134

    def test_none_when_amount_missing(self):
        f = Fermentable()
        f._yield = 1
        assert f.gu() is None

    def test_none_when_yield_missing(self):
        f = Fermentable()
        f.amount = 1
        assert f.gu() is None

    def test_scales_with_volume(self):
        f = Fermentable()
        f._yield = 80
        f.amount = 5
        gu_5l = f.gu(5)
        gu_10l = f.gu(10)
        assert gu_5l is not None and gu_10l is not None
        assert round(gu_5l, 4) == round(gu_10l * 2, 4)


class TestRecommendMash:
    def test_setter_casts_to_bool(self):
        f = Fermentable()
        f.recommend_mash = "TRUE"
        assert f.recommend_mash is True

        f.recommend_mash = "false"
        assert f.recommend_mash is False

    def test_default_is_none(self):
        assert Fermentable().recommend_mash is None
