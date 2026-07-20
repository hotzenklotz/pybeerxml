import os

from pybeerxml import Parser, Serializer
from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.recipe import Recipe
from pybeerxml.yeast import Yeast

RECIPE_PATH = os.path.join(os.path.dirname(__file__), "Simcoe IPA.xml")
RECIPE_PATH_3 = os.path.join(os.path.dirname(__file__), "CoffeeStout.xml")


def build_recipe():
    recipe = Recipe()
    recipe.name = "Test IPA"
    recipe.brewer = "Test Brewer"
    recipe.batch_size = 20.0
    recipe.og = 1.065
    recipe.forced_carbonation = True

    hop = Hop()
    hop.name = "Simcoe"
    hop.alpha = 13.0
    hop.amount = 0.05
    hop.use = "boil"
    hop.time = 60
    recipe.hops.append(hop)

    fermentable = Fermentable()
    fermentable.name = "Pale Malt"
    fermentable.amount = 5.0
    fermentable.yield_ = 80.0
    fermentable.recommend_mash = True
    recipe.fermentables.append(fermentable)

    yeast = Yeast()
    yeast.name = "US-05"
    yeast.attenuation = 78.0
    yeast.amount_is_weight = True
    recipe.yeasts.append(yeast)

    return recipe


def test_serialize_to_string_structure():
    xml = Serializer().serialize_to_string(build_recipe())

    assert xml.startswith("<?xml")
    assert "<RECIPES>" in xml
    assert "<RECIPE>" in xml
    assert "<NAME>Test IPA</NAME>" in xml
    assert "<HOPS>" in xml
    assert "<HOP>" in xml
    assert "<NAME>Simcoe</NAME>" in xml


def test_serialize_stored_og():
    xml = Serializer().serialize_to_string(build_recipe())
    assert "<OG>1.065</OG>" in xml


def test_serialize_omits_unset_fields():
    recipe = Recipe()
    recipe.name = "Minimal"
    xml = Serializer().serialize_to_string(recipe)

    # no stored OG -> no OG element
    assert "<OG>" not in xml
    assert "<FG>" not in xml
    assert "<IBU>" not in xml
    # calculated values are never serialized
    assert "CALCULATED" not in xml
    assert "PLATO" not in xml


def test_serialize_booleans_uppercase():
    xml = Serializer().serialize_to_string(build_recipe())
    assert "<FORCED_CARBONATION>TRUE</FORCED_CARBONATION>" in xml
    assert "<RECOMMEND_MASH>TRUE</RECOMMEND_MASH>" in xml
    assert "<AMOUNT_IS_WEIGHT>TRUE</AMOUNT_IS_WEIGHT>" in xml


def test_serialize_yield_field():
    xml = Serializer().serialize_to_string(build_recipe())
    assert "<YIELD>80.0</YIELD>" in xml


def test_serialize_accepts_single_recipe():
    xml = Serializer().serialize_to_string(build_recipe())
    assert xml.count("<RECIPE>") == 1


def test_serialize_to_file(tmp_path):
    path = tmp_path / "out.beerxml"
    Serializer().serialize(build_recipe(), path)

    recipes = Parser().parse(str(path))
    assert len(recipes) == 1
    assert recipes[0].name == "Test IPA"


def test_round_trip_from_fixture():
    original = Parser().parse(RECIPE_PATH_3)[0]

    xml = Serializer().serialize_to_string([original])
    restored = Parser().parse_from_string(xml)[0]

    assert restored.name == original.name
    assert restored.brewer == original.brewer
    assert restored.batch_size == original.batch_size
    assert restored.og_ == original.og_
    assert restored.fg_ == original.fg_
    assert restored.ibu_ == original.ibu_
    assert restored.abv_ == original.abv_
    assert restored.color_ == original.color_
    assert restored.forced_carbonation == original.forced_carbonation
    assert restored.est_color == original.est_color

    assert len(restored.hops) == len(original.hops)
    assert restored.hops[0].name == original.hops[0].name
    assert restored.hops[0].alpha == original.hops[0].alpha

    assert len(restored.fermentables) == len(original.fermentables)
    assert restored.fermentables[0].name == original.fermentables[0].name
    assert restored.fermentables[0].yield_ == original.fermentables[0].yield_
    assert restored.fermentables[0].recommend_mash == original.fermentables[0].recommend_mash

    assert len(restored.yeasts) == len(original.yeasts)
    assert restored.yeasts[0].name == original.yeasts[0].name
    assert restored.yeasts[0].product_id == original.yeasts[0].product_id
    assert restored.yeasts[0].amount_is_weight == original.yeasts[0].amount_is_weight

    assert len(restored.miscs) == len(original.miscs)
    assert restored.miscs[0].name == original.miscs[0].name
    assert restored.miscs[0].amount_is_weight == original.miscs[0].amount_is_weight

    assert restored.style.name == original.style.name
    assert restored.equipment.name == original.equipment.name
    assert restored.equipment.calc_boil_volume == original.equipment.calc_boil_volume
    assert restored.mash.name == original.mash.name
    assert len(restored.mash.steps) == len(original.mash.steps)
    assert restored.mash.steps[0].step_temp == original.mash.steps[0].step_temp


def test_round_trip_preserves_calculated_values():
    original = Parser().parse(RECIPE_PATH)[0]

    xml = Serializer().serialize_to_string([original])
    restored = Parser().parse_from_string(xml)[0]

    assert round(restored.og_calculated, 4) == round(original.og_calculated, 4)
    assert round(restored.fg_calculated, 4) == round(original.fg_calculated, 4)
    assert round(restored.ibu_calculated, 2) == round(original.ibu_calculated, 2)
    assert round(restored.abv_calculated, 2) == round(original.abv_calculated, 2)
    assert round(restored.color_calculated, 2) == round(original.color_calculated, 2)


def test_compat_aliases_round_trip():
    recipe = Recipe()
    recipe._og = 1.05
    assert recipe.og_ == 1.05
    assert recipe.og == 1.05

    xml = Serializer().serialize_to_string(recipe)
    assert "<OG>1.05</OG>" in xml

    restored = Parser().parse_from_string(xml)[0]
    assert restored._og == 1.05
