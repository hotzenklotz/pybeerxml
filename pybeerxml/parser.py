from __future__ import annotations

import logging
from typing import Any
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

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


class Parser:
    """Reads BeerXML files or strings and returns a list of `Recipe` objects.

    A single BeerXML document may contain multiple `<RECIPE>` elements; all
    three parse methods always return a list.  Unknown XML fields are logged at
    ``ERROR`` level and silently ignored so that non-standard files do not raise.

    Examples:
        >>> from pybeerxml import Parser
        >>> parser = Parser()
        >>> recipes = parser.parse("recipe.beerxml")
        >>> for recipe in recipes:
        ...     print(recipe.name, recipe.og)
    """

    def nodes_to_object(self, nodes: Element, beerxml_object: BeerXMLObject) -> None:
        """Map all child XML nodes onto an object's attributes.

        Args:
            nodes: Parent XML element whose children will be mapped.
            beerxml_object: Target object to receive the attribute values.
        """
        for node in nodes:
            self.node_to_object(node, beerxml_object)

    def node_to_object(self, node: Element, beerxml_object: BeerXMLObject) -> None:
        """Map a single XML node onto an object attribute.

        The node tag is lower-cased and used as the attribute name.  Numeric
        string values are coerced to ``float`` automatically.  The BeerXML
        field ``YIELD`` is mapped to ``_yield`` because ``yield`` is a Python
        keyword.

        Args:
            node: XML element to map.
            beerxml_object: Target object to receive the attribute value.
        """
        attribute = to_lower(node.tag)
        attribute = "_yield" if attribute == "yield" else attribute

        value: str | float | None = node.text or None

        if value is not None:
            try:
                value = float(value)
            except ValueError:
                pass

            try:
                setattr(beerxml_object, attribute, value)
            except AttributeError:
                logger.error("Attribute %s not supported.", attribute)

    def parse_from_string(self, xml_string: str) -> list[Recipe]:
        """Parse BeerXML content from a string.

        Args:
            xml_string: A valid BeerXML document as a string.

        Returns:
            A list of `Recipe` objects found in the document.

        Raises:
            xml.etree.ElementTree.ParseError: If ``xml_string`` is not valid XML.
        """
        tree = ElementTree.ElementTree(ElementTree.fromstring(xml_string))
        return self.parse_tree(tree)

    def parse(self, xml_file: str) -> list[Recipe]:
        """Parse a BeerXML file from disk.

        Args:
            xml_file: Path to the ``.beerxml`` file.

        Returns:
            A list of `Recipe` objects found in the file.

        Raises:
            FileNotFoundError: If ``xml_file`` does not exist.
            xml.etree.ElementTree.ParseError: If the file is not valid XML.
        """
        with open(xml_file, "rt") as file:
            tree = ElementTree.parse(file)
        return self.parse_tree(tree)

    def parse_tree(self, tree: ElementTree.ElementTree[Any]) -> list[Recipe]:
        """Parse an already-constructed ``ElementTree``.

        Useful when you need full control over XML loading (e.g. custom
        encoding handling).

        Args:
            tree: A parsed XML tree.

        Returns:
            A list of `Recipe` objects found in the tree.
        """
        recipes = []
        for recipe_node in tree.iter():
            if to_lower(recipe_node.tag) != "recipe":
                continue
            recipe = self.parse_recipe(recipe_node)
            recipes.append(recipe)
        return recipes

    def parse_recipe(self, recipe_node: Element) -> Recipe:
        """Parse a single ``<RECIPE>`` element into a `Recipe` object.

        Args:
            recipe_node: The ``<RECIPE>`` XML element.

        Returns:
            A populated `Recipe` instance.
        """
        recipe = Recipe()

        for recipe_property in recipe_node:
            tag_name = to_lower(recipe_property.tag)

            if tag_name == "fermentables":
                for fermentable_node in recipe_property:
                    fermentable = Fermentable()
                    self.nodes_to_object(fermentable_node, fermentable)
                    recipe.fermentables.append(fermentable)

            elif tag_name == "yeasts":
                for yeast_node in recipe_property:
                    yeast = Yeast()
                    self.nodes_to_object(yeast_node, yeast)
                    recipe.yeasts.append(yeast)

            elif tag_name == "hops":
                for hop_node in recipe_property:
                    hop = Hop()
                    self.nodes_to_object(hop_node, hop)
                    recipe.hops.append(hop)

            elif tag_name == "miscs":
                for misc_node in recipe_property:
                    misc = Misc()
                    self.nodes_to_object(misc_node, misc)
                    recipe.miscs.append(misc)

            elif tag_name == "style":
                style = Style()
                recipe.style = style
                self.nodes_to_object(recipe_property, style)

            elif tag_name == "waters":
                for water_node in recipe_property:
                    water = Water()
                    self.nodes_to_object(water_node, water)
                    recipe.waters.append(water)

            elif tag_name == "equipment":
                equipment = Equipment()
                recipe.equipment = equipment
                self.nodes_to_object(recipe_property, equipment)

            elif tag_name == "mash":
                mash = Mash()
                recipe.mash = mash
                for mash_node in recipe_property:
                    if to_lower(mash_node.tag) == "mash_steps":
                        for mash_step_node in mash_node:
                            mash_step = MashStep()
                            self.nodes_to_object(mash_step_node, mash_step)
                            mash.steps.append(mash_step)
                    else:
                        self.node_to_object(mash_node, mash)

            else:
                self.node_to_object(recipe_property, recipe)

        return recipe
