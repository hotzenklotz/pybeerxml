from __future__ import annotations

import logging
from typing import Any
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from pybeerxml.document import RecipesDocument
from pybeerxml.equipment import Equipment
from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.mash_step import MashStep
from pybeerxml.misc import Misc
from pybeerxml.recipe import Recipe
from pybeerxml.style import Style
from pybeerxml.utils import to_lower
from pybeerxml.water import Water
from pybeerxml.yeast import Yeast

logger = logging.getLogger(__name__)

BeerXMLObject = Recipe | Mash | Yeast | Fermentable | Hop | Misc | MashStep | Style | Water | Equipment
INTEGER_FIELDS = {"version", "fermentation_stages", "times_cultured", "max_reuse"}
TEXT_FIELDS = {"category_number"}


class Parser:
    """Reads BeerXML files or strings and returns a list of `Recipe` objects.

    A single BeerXML document may contain multiple `<RECIPE>` elements; all
    three parse methods always return a list. Unknown XML fields are logged at
    ``ERROR`` level and silently ignored so that non-standard files do not
    raise.

    Examples:
        >>> from pybeerxml import Parser
        >>> parser = Parser()
        >>> recipes = parser.parse("recipe.beerxml")
        >>> for recipe in recipes:
        ...     print(recipe.name, recipe.og)
    """

    
    def parse_from_string(self, xml_string: str) -> list[Recipe]:
        """Parse BeerXML content from a string.

        Args:
            xml_string: A valid BeerXML document as a string.

        Returns:
            A list of `Recipe` objects found in the document.
        """
        return RecipesDocument.from_xml(xml_string).recipes

    def parse(self, xml_file: str) -> list[Recipe]:
        """Parse a BeerXML file from disk.

        Args:
            xml_file: Path to the `.beerxml` file.

        Returns:
            A list of `Recipe` objects found in the file.
        """
        with open(xml_file, "rt") as file:
            return self.parse_from_string(file.read())

    