from __future__ import annotations

import logging
from typing import Any
from xml.etree import ElementTree

from pybeerxml.recipe import Recipe, Recipes

__all__ = ["Parser", "Recipe"]

logger = logging.getLogger(__name__)


class Parser:
    """Reads BeerXML files or strings and returns a list of `Recipe` objects.

    A single BeerXML document may contain multiple ``<RECIPE>`` elements; all
    parse methods always return a list.  Unknown XML fields are silently
    ignored so that non-standard files do not raise.

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

        Raises:
            pydantic_core._pydantic_core.ValidationError: If ``xml_string`` is
                not valid XML or does not match the BeerXML schema.
        """
        return Recipes.from_xml(xml_string).recipes

    def parse(self, xml_file: str) -> list[Recipe]:
        """Parse a BeerXML file from disk.

        Args:
            xml_file: Path to the ``.beerxml`` file.

        Returns:
            A list of `Recipe` objects found in the file.

        Raises:
            FileNotFoundError: If ``xml_file`` does not exist.
            pydantic_core._pydantic_core.ValidationError: If the file is not
                valid XML or does not match the BeerXML schema.
        """
        with open(xml_file, "rt") as file:
            return self.parse_from_string(file.read())

    def parse_tree(self, tree: ElementTree.ElementTree[Any]) -> list[Recipe]:
        """Parse an already-constructed ``ElementTree``.

        Useful when you need full control over XML loading (e.g. custom
        encoding handling).

        Args:
            tree: A parsed XML tree.

        Returns:
            A list of `Recipe` objects found in the tree.
        """
        xml_string = ElementTree.tostring(tree.getroot(), encoding="unicode")
        return self.parse_from_string(xml_string)
