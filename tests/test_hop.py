import pytest
from pybeerxml.hop import Hop


def test_utilization_factor():

    hop = Hop()

    hop.form = "pellet"
    assert hop.utilization_factor() == 1.15

    hop.form = "whole"
    assert hop.utilization_factor() == 1


def test_bitterness():

    hop = Hop()
    hop.time = 60  # Minutes
    hop.amount = 0.010  # KG
    hop.alpha = 10

    original_gravity = 1.050  # OG
    batch_size = 5  # liter

    bitterness = hop.bitterness("tinseth", original_gravity, batch_size)
    assert bitterness == 46.132815450219816

    bitterness = hop.bitterness("rager", original_gravity, batch_size)
    assert bitterness == 61.63901270302538

    with pytest.raises(Exception):
        hop.bitterness("", original_gravity, batch_size)
