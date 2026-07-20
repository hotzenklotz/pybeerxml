from __future__ import annotations

import os
import xml.dom.minidom

from pybeerxml.recipe import Recipe, Recipes


class Serializer:
    """Writes `Recipe` objects to BeerXML files or strings.

    Only values stored in the XML-backed fields are serialized — calculated
    properties (``og_calculated``, ``og_plato``, etc.) are never written.
    Fields that are ``None`` are omitted from the output, and boolean fields
    are emitted as ``TRUE`` / ``FALSE`` per the BeerXML spec.

    Examples:
        >>> from pybeerxml import Parser, Serializer
        >>> recipes = Parser().parse("recipe.beerxml")
        >>> Serializer().serialize(recipes, "copy.beerxml")
    """

    def serialize_to_string(self, recipes: Recipe | list[Recipe]) -> str:
        """Serialize recipes to a BeerXML document string.

        Args:
            recipes: A single `Recipe` or a list of `Recipe` objects.

        Returns:
            A pretty-printed BeerXML document as a string, including the XML
            declaration.
        """
        if isinstance(recipes, Recipe):
            recipes = [recipes]
        document = Recipes(recipes=recipes)
        raw_xml = document.to_xml(exclude_none=True)
        return xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="  ")

    def serialize(self, recipes: Recipe | list[Recipe], xml_file: str | os.PathLike) -> None:
        """Serialize recipes to a BeerXML file on disk.

        Args:
            recipes: A single `Recipe` or a list of `Recipe` objects.
            xml_file: Destination path, e.g. ``"recipe.beerxml"``. Existing
                files are overwritten.
        """
        with open(xml_file, "w", encoding="utf-8") as file:
            file.write(self.serialize_to_string(recipes))
