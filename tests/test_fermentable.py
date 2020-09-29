import pytest
from pybeerxml.fermentable import Fermentable


def test_add_after_boil():

    fermentable = Fermentable()
    fermentable.add_after_boil = True

    assert fermentable.add_after_boil == True


def test_ppg():

    fermentable = Fermentable()
    fermentable._yield = 1

    assert fermentable.ppg == 0.46214


def test_addition():

    fermentable = Fermentable()

    fermentable.name = "Munich Malt"
    assert fermentable.addition == "steep"

    fermentable.name = "Honey"
    assert fermentable.addition == "boil"

    fermentable.name = None
    assert fermentable.addition == "mash"


def test_gu():

    fermentable = Fermentable()
    fermentable._yield = 1
    fermentable.amount = 1  # kg

    assert fermentable.gu() == 3.8567413912148134
