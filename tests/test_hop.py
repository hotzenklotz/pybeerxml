import pytest

from pybeerxml.hop import Hop


class TestUtilizationFactor:
    def test_pellet(self):
        h = Hop()
        h.form = "pellet"
        assert h.utilization_factor() == 1.15

    def test_whole(self):
        h = Hop()
        h.form = "whole"
        assert h.utilization_factor() == 1.0

    def test_none_defaults_to_whole(self):
        assert Hop().utilization_factor() == 1.0


class TestBitterness:
    @pytest.fixture
    def hop(self):
        h = Hop()
        h.time = 60
        h.amount = 0.010  # kg
        h.alpha = 10
        return h

    def test_tinseth(self, hop):
        assert hop.bitterness("tinseth", 1.050, 5) == 46.132815450219816

    def test_rager(self, hop):
        assert hop.bitterness("rager", 1.050, 5) == 61.63901270302538

    def test_rager_with_high_og_applies_adjustment(self, hop):
        # OG > 1.05 triggers a gravity adjustment that reduces bitterness
        low_og = hop.bitterness("rager", 1.050, 5)
        high_og = hop.bitterness("rager", 1.080, 5)
        assert high_og < low_og

    def test_unknown_method_raises_value_error(self, hop):
        with pytest.raises(ValueError, match="Unknown IBU method"):
            hop.bitterness("unknown", 1.050, 5)

    def test_missing_time_raises_value_error(self):
        h = Hop()
        h.alpha = 10
        h.amount = 0.010
        with pytest.raises(ValueError):
            h.bitterness("tinseth", 1.050, 5)

    def test_missing_alpha_raises_value_error(self):
        h = Hop()
        h.time = 60
        h.amount = 0.010
        with pytest.raises(ValueError):
            h.bitterness("tinseth", 1.050, 5)

    def test_missing_amount_raises_value_error(self):
        h = Hop()
        h.time = 60
        h.alpha = 10
        with pytest.raises(ValueError):
            h.bitterness("tinseth", 1.050, 5)
