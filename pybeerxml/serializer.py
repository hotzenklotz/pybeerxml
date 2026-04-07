from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from pybeerxml.document import RecipesDocument
from pybeerxml.recipe import Recipe

REQUIRED_RECIPE_SECTIONS = ("HOPS", "FERMENTABLES", "MISCS", "YEASTS", "WATERS")


def recipe_to_xml_element(recipe: Recipe) -> Element:
    element = recipe.to_xml_tree(skip_empty=True)
    _ensure_required_recipe_sections(element)
    return element


def serialize(recipes: list[Recipe], encoding: str = "utf-8", xml_declaration: bool = True) -> str:
    document = RecipesDocument(recipes=recipes)
    root = document.to_xml_tree(skip_empty=True)
    for recipe_node in root.findall("RECIPE"):
        _ensure_required_recipe_sections(recipe_node)
    xml = ElementTree.tostring(
        root,
        encoding=encoding if xml_declaration else "unicode",
        xml_declaration=xml_declaration,
    )
    return xml if isinstance(xml, str) else xml.decode(encoding)


def write(recipes: list[Recipe], path: str, encoding: str = "utf-8") -> None:
    xml = serialize(recipes, encoding=encoding, xml_declaration=True)
    Path(path).write_text(xml, encoding=encoding)


def _ensure_required_recipe_sections(recipe_element: Element) -> None:
    for tag in REQUIRED_RECIPE_SECTIONS:
        if recipe_element.find(tag) is None:
            recipe_element.append(Element(tag))
