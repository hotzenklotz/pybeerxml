import os
from xml.etree import ElementTree

from pybeerxml import Parser, Serializer
from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.misc import Misc
from pybeerxml.recipe import Recipe
from pybeerxml.yeast import Yeast

RECIPE_PATH_1 = os.path.join(os.path.dirname(__file__), "Simcoe IPA.xml")
RECIPE_PATH_2 = os.path.join(os.path.dirname(__file__), "Oatmeal Stout.xml")
RECIPE_PATH_3 = os.path.join(os.path.dirname(__file__), "CoffeeStout.xml")


RECIPE_FIELDS = (
    "name",
    "version",
    "type",
    "brewer",
    "asst_brewer",
    "batch_size",
    "boil_size",
    "boil_time",
    "efficiency",
    "notes",
    "taste_notes",
    "taste_rating",
    "date",
    "_og",
    "_fg",
    "_ibu",
    "_abv",
    "_color",
    "fermentation_stages",
    "primary_age",
    "primary_temp",
    "secondary_age",
    "secondary_temp",
    "tertiary_age",
    "tertiary_temp",
    "age",
    "age_temp",
    "carbonation",
    "forced_carbonation",
    "priming_sugar_name",
    "carbonation_temp",
    "priming_sugar_equiv",
    "keg_priming_factor",
    "est_og",
    "est_fg",
    "est_color",
    "ibu_method",
    "est_abv",
    "actual_efficiency",
    "calories",
    "carbonation_used",
)

STYLE_FIELDS = (
    "name",
    "category",
    "version",
    "category_number",
    "style_letter",
    "style_guide",
    "type",
    "og_min",
    "og_max",
    "fg_min",
    "fg_max",
    "ibu_min",
    "ibu_max",
    "color_min",
    "color_max",
    "abv_min",
    "abv_max",
    "carb_min",
    "carb_max",
    "notes",
)

EQUIPMENT_FIELDS = (
    "name",
    "version",
    "boil_size",
    "batch_size",
    "tun_volume",
    "tun_weight",
    "tun_specific_heat",
    "top_up_water",
    "trub_chiller_loss",
    "evap_rate",
    "boil_time",
    "calc_boil_volume",
    "lauter_deadspace",
    "top_up_kettle",
    "hop_utilization",
    "notes",
)

HOP_FIELDS = (
    "name",
    "version",
    "alpha",
    "amount",
    "use",
    "time",
    "notes",
    "type",
    "form",
    "beta",
    "hsi",
    "origin",
    "substitutes",
    "humulene",
    "caryophyllene",
    "cohumulone",
    "myrcene",
)

FERMENTABLE_FIELDS = (
    "name",
    "version",
    "type",
    "amount",
    "_yield",
    "color",
    "add_after_boil",
    "origin",
    "supplier",
    "notes",
    "coarse_fine_diff",
    "moisture",
    "diastatic_power",
    "protein",
    "max_in_batch",
    "recommend_mash",
    "ibu_gal_per_lb",
)

MISC_FIELDS = (
    "name",
    "version",
    "type",
    "use",
    "time",
    "amount",
    "amount_is_weight",
    "use_for",
    "notes",
)

YEAST_FIELDS = (
    "name",
    "version",
    "type",
    "form",
    "amount",
    "amount_is_weight",
    "laboratory",
    "product_id",
    "min_temperature",
    "max_temperature",
    "flocculation",
    "attenuation",
    "notes",
    "best_for",
    "times_cultured",
    "max_reuse",
    "inventory",
    "culture_date",
    "add_to_secondary",
)

WATER_FIELDS = (
    "name",
    "version",
    "amount",
    "calcium",
    "bicarbonate",
    "sulfate",
    "chloride",
    "sodium",
    "magnesium",
    "ph",
    "notes",
    "volume",
)

MASH_FIELDS = (
    "name",
    "version",
    "grain_temp",
    "sparge_temp",
    "ph",
    "tun_temp",
    "tun_weight",
    "tun_specific_heat",
    "equip_adjust",
    "notes",
)

MASH_STEP_FIELDS = (
    "name",
    "version",
    "type",
    "infuse_amount",
    "step_temp",
    "step_time",
    "end_temp",
    "decoction_amt",
)


def _snapshot_fields(obj, fields):
    if obj is None:
        return None
    return {field: getattr(obj, field) for field in fields}


def _snapshot_recipe(recipe):
    return {
        "recipe": _snapshot_fields(recipe, RECIPE_FIELDS),
        "style": _snapshot_fields(recipe.style, STYLE_FIELDS),
        "equipment": _snapshot_fields(recipe.equipment, EQUIPMENT_FIELDS),
        "hops": [_snapshot_fields(hop, HOP_FIELDS) for hop in recipe.hops],
        "fermentables": [_snapshot_fields(fermentable, FERMENTABLE_FIELDS) for fermentable in recipe.fermentables],
        "miscs": [_snapshot_fields(misc, MISC_FIELDS) for misc in recipe.miscs],
        "yeasts": [_snapshot_fields(yeast, YEAST_FIELDS) for yeast in recipe.yeasts],
        "waters": [_snapshot_fields(water, WATER_FIELDS) for water in recipe.waters],
        "mash": {
            "fields": _snapshot_fields(recipe.mash, MASH_FIELDS),
            "steps": [_snapshot_fields(step, MASH_STEP_FIELDS) for step in (recipe.mash.steps if recipe.mash else [])],
        },
    }


def test_roundtrip_simcoe_recipe():
    parser = Parser()
    recipe = parser.parse(RECIPE_PATH_1)[0]

    xml = recipe.to_xml_string()
    roundtripped = parser.parse_from_string(xml)[0]

    assert _snapshot_recipe(roundtripped) == _snapshot_recipe(recipe)


def test_roundtrip_oatmeal_stout_recipe():
    parser = Parser()
    recipe = parser.parse(RECIPE_PATH_2)[0]

    xml = recipe.to_xml_string()
    roundtripped = parser.parse_from_string(xml)[0]

    assert _snapshot_recipe(roundtripped) == _snapshot_recipe(recipe)


def test_roundtrip_coffee_stout_recipe():
    parser = Parser()
    recipe = parser.parse(RECIPE_PATH_3)[0]

    xml = recipe.to_xml_string()
    roundtripped = parser.parse_from_string(xml)[0]

    assert _snapshot_recipe(roundtripped) == _snapshot_recipe(recipe)


def test_serialize_multiple_recipes_in_one_document():
    parser = Parser()
    recipes = [parser.parse(RECIPE_PATH_1)[0], parser.parse(RECIPE_PATH_2)[0]]
    serializer = Serializer()

    xml = serializer.serialize(recipes)
    tree = ElementTree.fromstring(xml)
    roundtripped = parser.parse_from_string(xml)

    assert tree.tag == "RECIPES"
    assert len(tree.findall("RECIPE")) == 2
    assert [recipe.name for recipe in roundtripped] == [recipe.name for recipe in recipes]


def test_numeric_boolean_and_backing_field_serialization():
    recipe = Recipe()
    recipe.name = "Serialization Test"
    recipe.version = 1
    recipe.batch_size = 20.5
    recipe.forced_carbonation = True

    fermentable = Fermentable()
    fermentable.name = "Pale Malt"
    fermentable.version = 1
    fermentable.amount = 5.25
    fermentable._yield = 81.0
    fermentable.color = 3.0
    fermentable.add_after_boil = False
    fermentable.recommend_mash = True
    recipe.fermentables.append(fermentable)

    misc = Misc()
    misc.name = "Irish Moss"
    misc.type = "Fining"
    misc.amount = 0.01
    misc.amount_is_weight = True
    recipe.miscs.append(misc)

    yeast = Yeast()
    yeast.name = "US-05"
    yeast.amount = 0.011
    yeast.amount_is_weight = False
    recipe.yeasts.append(yeast)

    xml = recipe.to_xml_string()

    assert "<VERSION>1</VERSION>" in xml
    assert "<BATCH_SIZE>20.5</BATCH_SIZE>" in xml
    assert "<FORCED_CARBONATION>TRUE</FORCED_CARBONATION>" in xml
    assert "<YIELD>81</YIELD>" in xml
    assert "<ADD_AFTER_BOIL>FALSE</ADD_AFTER_BOIL>" in xml
    assert "<RECOMMEND_MASH>TRUE</RECOMMEND_MASH>" in xml
    assert "<AMOUNT_IS_WEIGHT>TRUE</AMOUNT_IS_WEIGHT>" in xml
    assert "<AMOUNT_IS_WEIGHT>FALSE</AMOUNT_IS_WEIGHT>" in xml


def test_calculated_recipe_metrics_are_not_serialized_when_only_derived():
    recipe = Recipe()
    recipe.name = "Derived Metrics Only"
    recipe.batch_size = 20.0

    fermentable = Fermentable()
    fermentable.name = "Pale Malt"
    fermentable.amount = 5.0
    fermentable._yield = 80.0
    fermentable.color = 5.0
    recipe.fermentables.append(fermentable)

    hop = Hop()
    hop.name = "Cascade"
    hop.alpha = 6.0
    hop.amount = 0.02
    hop.use = "boil"
    hop.time = 60.0
    recipe.hops.append(hop)

    yeast = Yeast()
    yeast.name = "House Yeast"
    yeast.attenuation = 75.0
    recipe.yeasts.append(yeast)

    assert recipe.og is not None
    assert recipe.fg is not None
    assert recipe.ibu is not None
    assert recipe.abv is not None
    assert recipe.color is not None

    xml = recipe.to_xml_string()
    recipe_node = ElementTree.fromstring(xml).find("RECIPE")
    roundtripped = Parser().parse_from_string(xml)[0]

    assert recipe_node is not None
    assert recipe_node.find("OG") is None
    assert recipe_node.find("FG") is None
    assert recipe_node.find("IBU") is None
    assert recipe_node.find("ABV") is None
    assert recipe_node.find("COLOR") is None
    assert roundtripped._og is None
    assert roundtripped._fg is None
    assert roundtripped._ibu is None
    assert roundtripped._abv is None
    assert roundtripped._color is None
    assert round(roundtripped.og, 4) == round(recipe.og, 4)
    assert round(roundtripped.fg, 4) == round(recipe.fg, 4)
    assert round(roundtripped.ibu, 4) == round(recipe.ibu, 4)
    assert round(roundtripped.abv, 4) == round(recipe.abv, 4)
    assert round(roundtripped.color, 4) == round(recipe.color, 4)


def test_empty_optional_sections_are_omitted():
    recipe = Recipe()
    recipe.name = "Bare Minimum"

    xml = recipe.to_xml_string()

    assert "<HOPS />" in xml or "<HOPS/>" in xml
    assert "<FERMENTABLES />" in xml or "<FERMENTABLES/>" in xml
    assert "<MISCS />" in xml or "<MISCS/>" in xml
    assert "<YEASTS />" in xml or "<YEASTS/>" in xml
    assert "<WATERS />" in xml or "<WATERS/>" in xml
    assert "<MASH>" not in xml


def test_recipe_element_and_write_helpers(tmp_path):
    recipe = Parser().parse(RECIPE_PATH_1)[0]
    serializer = Serializer()
    single_path = tmp_path / "single.xml"
    multiple_path = tmp_path / "multiple.xml"

    recipe_element = recipe.to_xml_element()
    recipe.write_xml(str(single_path))
    serializer.write([recipe, Parser().parse(RECIPE_PATH_2)[0]], str(multiple_path))

    assert recipe_element.tag == "RECIPE"
    assert Parser().parse(str(single_path))[0].name == recipe.name
    assert len(Parser().parse(str(multiple_path))) == 2


def test_serializer_class_writes_file(tmp_path):
    serializer = Serializer()
    recipes = [Parser().parse(RECIPE_PATH_1)[0]]
    output_path = tmp_path / "serializer.xml"

    xml = serializer.serialize(recipes)
    serializer.write(recipes, str(output_path))

    assert "<RECIPES>" in xml
    assert Parser().parse(str(output_path))[0].name == recipes[0].name


def test_parser_preserves_integer_version_fields():
    xml = """<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
  <RECIPE>
    <NAME>Version Test</NAME>
    <VERSION>1</VERSION>
    <TYPE>All Grain</TYPE>
    <STYLE>
      <NAME>Ordinary Bitter</NAME>
      <CATEGORY>British Bitter</CATEGORY>
      <VERSION>1</VERSION>
      <CATEGORY_NUMBER>11</CATEGORY_NUMBER>
      <STYLE_LETTER>A</STYLE_LETTER>
      <STYLE_GUIDE>BJCP</STYLE_GUIDE>
      <TYPE>Ale</TYPE>
      <OG_MIN>1.030</OG_MIN>
      <OG_MAX>1.039</OG_MAX>
      <FG_MIN>1.007</FG_MIN>
      <FG_MAX>1.011</FG_MAX>
      <IBU_MIN>25</IBU_MIN>
      <IBU_MAX>35</IBU_MAX>
      <COLOR_MIN>4</COLOR_MIN>
      <COLOR_MAX>14</COLOR_MAX>
    </STYLE>
    <BREWER>Tester</BREWER>
    <BATCH_SIZE>20</BATCH_SIZE>
    <BOIL_SIZE>25</BOIL_SIZE>
    <BOIL_TIME>60</BOIL_TIME>
    <EFFICIENCY>75</EFFICIENCY>
    <HOPS />
    <FERMENTABLES />
    <MISCS>
      <MISC>
        <NAME>Irish Moss</NAME>
        <VERSION>1</VERSION>
        <TYPE>Fining</TYPE>
        <USE>Boil</USE>
        <TIME>15</TIME>
        <AMOUNT>0.01</AMOUNT>
      </MISC>
    </MISCS>
    <YEASTS />
    <WATERS>
      <WATER>
        <NAME>RO Water</NAME>
        <VERSION>1</VERSION>
        <AMOUNT>20</AMOUNT>
        <CALCIUM>0</CALCIUM>
        <BICARBONATE>0</BICARBONATE>
        <SULFATE>0</SULFATE>
        <CHLORIDE>0</CHLORIDE>
        <SODIUM>0</SODIUM>
        <MAGNESIUM>0</MAGNESIUM>
      </WATER>
    </WATERS>
    <MASH>
      <NAME>Single Infusion</NAME>
      <VERSION>1</VERSION>
      <GRAIN_TEMP>22</GRAIN_TEMP>
      <MASH_STEPS>
        <MASH_STEP>
          <NAME>Conversion</NAME>
          <VERSION>1</VERSION>
          <TYPE>Infusion</TYPE>
          <INFUSE_AMOUNT>10</INFUSE_AMOUNT>
          <STEP_TEMP>67</STEP_TEMP>
          <STEP_TIME>60</STEP_TIME>
        </MASH_STEP>
      </MASH_STEPS>
    </MASH>
  </RECIPE>
</RECIPES>
"""
    recipe = Parser().parse_from_string(xml)[0]

    assert isinstance(recipe.version, int)
    assert isinstance(recipe.style.version, int)
    assert isinstance(recipe.miscs[0].version, int)
    assert isinstance(recipe.waters[0].version, int)
    assert isinstance(recipe.mash.version, int)
    assert isinstance(recipe.mash.steps[0].version, int)


def test_style_required_fields_roundtrip():
    style_xml = """<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
  <RECIPE>
    <NAME>x</NAME>
    <VERSION>1</VERSION>
    <TYPE>All Grain</TYPE>
    <STYLE>
      <NAME>Dry Stout</NAME>
      <CATEGORY>Stout</CATEGORY>
      <VERSION>1</VERSION>
      <CATEGORY_NUMBER>15</CATEGORY_NUMBER>
      <STYLE_LETTER>B</STYLE_LETTER>
      <STYLE_GUIDE>BJCP</STYLE_GUIDE>
      <TYPE>Ale</TYPE>
      <OG_MIN>1.036</OG_MIN>
      <OG_MAX>1.050</OG_MAX>
      <FG_MIN>1.007</FG_MIN>
      <FG_MAX>1.011</FG_MAX>
      <IBU_MIN>30</IBU_MIN>
      <IBU_MAX>45</IBU_MAX>
      <COLOR_MIN>25</COLOR_MIN>
      <COLOR_MAX>40</COLOR_MAX>
    </STYLE>
    <BREWER>x</BREWER>
    <BATCH_SIZE>1</BATCH_SIZE>
    <BOIL_SIZE>1</BOIL_SIZE>
    <BOIL_TIME>1</BOIL_TIME>
    <EFFICIENCY>1</EFFICIENCY>
    <HOPS />
    <FERMENTABLES />
    <MISCS />
    <YEASTS />
    <WATERS />
    <MASH>
      <NAME>x</NAME>
      <VERSION>1</VERSION>
      <GRAIN_TEMP>20</GRAIN_TEMP>
      <MASH_STEPS>
        <MASH_STEP>
          <NAME>x</NAME>
          <VERSION>1</VERSION>
          <TYPE>Infusion</TYPE>
          <STEP_TEMP>20</STEP_TEMP>
          <STEP_TIME>1</STEP_TIME>
        </MASH_STEP>
      </MASH_STEPS>
    </MASH>
  </RECIPE>
</RECIPES>
"""
    recipe = Recipe()
    recipe.name = "Style Fields"
    recipe.version = 1
    recipe.type = "All Grain"
    recipe.brewer = "Tester"
    recipe.batch_size = 20.0
    recipe.boil_size = 25.0
    recipe.boil_time = 60.0
    recipe.efficiency = 75.0
    recipe.style = Parser().parse_from_string(style_xml)[0].style

    xml = recipe.to_xml_string()
    roundtripped = Parser().parse_from_string(xml)[0]

    assert roundtripped.style.version == 1
    assert roundtripped.style.category_number == "15"
    assert roundtripped.style.style_letter == "B"
    assert roundtripped.style.style_guide == "BJCP"
    assert roundtripped.style.type == "Ale"
