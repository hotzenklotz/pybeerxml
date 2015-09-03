import pytest
import os
from pybeerxml import Parser, Recipe

RECIPE_PATH = os.path.join(os.path.dirname(__file__), "Simcoe IPA.xml")

class TestParser:

    def test_parse(self):

        recipe_parser = Parser()
        recipe = recipe_parser.parse(RECIPE_PATH)

        "should have at least one recipe"
        assert(len(recipe) > 0)

        "should be of type Recipe"
        assert(type(recipe[0]) is Recipe)

    def test_note_to_object(self):

        assert(False)

    def test_to_lower(self):

        recipe_parser = Parser()
        assert(recipe_parser.to_lower("MASH") == "mash")

        assert(recipe_parser.to_lower("") == "")

        assert(recipe_parser.to_lower(10) == "")

        assert(recipe_parser.to_lower(None) == "")




