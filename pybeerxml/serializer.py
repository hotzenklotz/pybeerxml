from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from pybeerxml.document import RecipesDocument
from pybeerxml.recipe import Recipe

REQUIRED_RECIPE_SECTIONS = ("HOPS", "FERMENTABLES", "MISCS", "YEASTS", "WATERS")


class Serializer:
    """Serialize `Recipe` objects into BeerXML.

    The API mirrors `Parser` on the write side:

    - `serialize()` returns a complete BeerXML document string
    - `write()` writes a complete BeerXML document to disk
    - `recipe_to_xml_element()` returns a single `<RECIPE>` element

    BeerXML requires recipe record-set containers such as `HOPS` and
    `FERMENTABLES`, so those sections are emitted even when empty.
    """

    def recipe_to_xml_element(self, recipe: Recipe) -> Element:
        """Serialize a single recipe as a BeerXML `<RECIPE>` element.

        Args:
            recipe: The recipe to serialize.

        Returns:
            A single `<RECIPE>` XML element.
        """
        element = recipe.to_xml_tree(skip_empty=True)
        _ensure_required_recipe_sections(element)
        return element

    def serialize(self, recipes: list[Recipe], encoding: str = "utf-8", xml_declaration: bool = True) -> str:
        """Serialize recipes into a complete BeerXML document string.

        Args:
            recipes: Recipes to include in the document.
            encoding: XML encoding to use for output.
            xml_declaration: Whether to include the XML declaration.

        Returns:
            A BeerXML document as a string.
        """
        document = RecipesDocument(recipes=recipes)
        root = document.to_xml_tree(skip_empty=True)
        for recipe_node in root.findall("RECIPE"):
            _ensure_required_recipe_sections(recipe_node)
        ElementTree.indent(root, space="  ")
        xml = ElementTree.tostring(
            root,
            encoding=encoding if xml_declaration else "unicode",
            xml_declaration=xml_declaration,
        )
        return xml if isinstance(xml, str) else xml.decode(encoding)

    def write(self, recipes: list[Recipe], path: str, encoding: str = "utf-8") -> None:
        """Write recipes to a BeerXML file.

        Args:
            recipes: Recipes to serialize.
            path: Destination file path.
            encoding: XML encoding to use for output.
        """
        xml = self.serialize(recipes, encoding=encoding, xml_declaration=True)
        Path(path).write_text(xml, encoding=encoding)


def _ensure_required_recipe_sections(recipe_element: Element) -> None:
    """Ensure BeerXML-required recipe container tags are present."""
    for tag in REQUIRED_RECIPE_SECTIONS:
        if recipe_element.find(tag) is None:
            recipe_element.append(Element(tag))
