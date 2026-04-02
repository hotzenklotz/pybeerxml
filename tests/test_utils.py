from pybeerxml.utils import cast_to_bool, gravity_to_plato, to_lower


class TestToLower:
    def test_uppercase(self):
        assert to_lower("MASH") == "mash"

    def test_empty_string(self):
        assert to_lower("") == ""

    def test_integer(self):
        assert to_lower(10) == ""

    def test_none(self):
        assert to_lower(None) == ""

    def test_mixed_case(self):
        assert to_lower("BeerXML") == "beerxml"


class TestCastToBool:
    def test_string_true(self):
        assert cast_to_bool("true") is True
        assert cast_to_bool("True") is True
        assert cast_to_bool("TRUE") is True

    def test_string_false(self):
        assert cast_to_bool("false") is False
        assert cast_to_bool("False") is False
        assert cast_to_bool("FALSE") is False

    def test_bool_passthrough(self):
        assert cast_to_bool(True) is True
        assert cast_to_bool(False) is False

    def test_numeric(self):
        assert cast_to_bool(1) is True
        assert cast_to_bool(0) is False
        assert cast_to_bool(1.0) is True
        assert cast_to_bool(0.0) is False

    def test_unknown_returns_false(self):
        assert cast_to_bool(None) is False
        assert cast_to_bool([]) is False
        assert cast_to_bool({}) is False


class TestGravityToPlato:
    def test_none_returns_none(self):
        assert gravity_to_plato(None) is None

    def test_water(self):
        # 1.000 SG = 0 Plato
        assert round(gravity_to_plato(1.000), 2) == 0.0

    def test_typical_og(self):
        # 1.050 SG ≈ 12.4 Plato
        result = gravity_to_plato(1.050)
        assert result is not None
        assert round(result, 1) == 12.4
