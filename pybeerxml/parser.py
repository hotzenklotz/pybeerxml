import logging
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import Union, List, Text

from pybeerxml.recipe import Recipe
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.mash_step import MashStep
from pybeerxml.misc import Misc
from pybeerxml.yeast import Yeast
from pybeerxml.water import Water
from pybeerxml.style import Style
from pybeerxml.equipment import Equipment
from pybeerxml.fermentable import Fermentable
from pybeerxml.utils import to_lower

logger = logging.getLogger("__name__")


class Parser:
    def nodes_to_object(
        self,
        nodes: Element,
        beerxml_object: Union[
            Recipe,
            Mash,
            Yeast,
            Fermentable,
            Hop,
            Misc,
            MashStep,
            Style,
            Water,
            Equipment,
        ],
    ):
        "Map all child nodes to an object's attributes"

        for node in list(nodes):
            self.node_to_object(node, beerxml_object)

    # pylint: disable=no-self-use
    def node_to_object(
        self,
        node: Element,
        beerxml_object: Union[
            Recipe,
            Mash,
            Yeast,
            Fermentable,
            Hop,
            Misc,
            MashStep,
            Style,
            Water,
            Equipment,
        ],
    ):
        "Map a single node to an object's attributes"

        attribute = to_lower(node.tag)

        # Yield is a protected keyword in Python, so let's rename it
        attribute = "_yield" if attribute == "yield" else attribute

        value: Union[Text, float, None] = node.text or None

        if value is not None:
            # XML numbers are represented as strings in some cases
            # try to parse as number if possible
            try:
                value = float(value)
            except ValueError:
                pass

            try:
                setattr(beerxml_object, attribute, value)
            except AttributeError:
                logger.error("Attribute %s not supported.", attribute)

    def parse_from_string(self, xml_string):
        "Get a list of parsed recipes from BeerXML string"
        tree = ElementTree.ElementTree(ElementTree.fromstring(xml_string))

        return self.parse_tree(tree)

    def parse(self, xml_file: Text) -> List[Recipe]:
        "Get a list of parsed recipes from BeerXML input"

        with open(xml_file, "rt") as file:
            tree = ElementTree.parse(file)

        return self.parse_tree(tree)

    def parse_tree(self, tree: ElementTree.ElementTree) -> List[Recipe]:
        recipes = []
        for recipe_node in tree.iter():
            if to_lower(recipe_node.tag) != "recipe":
                continue
            recipe = self.parse_recipe(recipe_node)
            recipes.append(recipe)

        return recipes

    # pylint: disable=too-many-branches, too-many-locals
    def parse_recipe(self, recipe_node: Element) -> Recipe:

        recipe = Recipe()

        for recipe_property in list(recipe_node):
            tag_name = to_lower(recipe_property.tag)

            if tag_name == "fermentables":
                for fermentable_node in list(recipe_property):
                    fermentable = Fermentable()
                    self.nodes_to_object(fermentable_node, fermentable)
                    recipe.fermentables.append(fermentable)

            elif tag_name == "yeasts":
                for yeast_node in list(recipe_property):
                    yeast = Yeast()
                    self.nodes_to_object(yeast_node, yeast)
                    recipe.yeasts.append(yeast)

            elif tag_name == "hops":
                for hop_node in list(recipe_property):
                    hop = Hop()
                    self.nodes_to_object(hop_node, hop)
                    recipe.hops.append(hop)

            elif tag_name == "miscs":
                for misc_node in list(recipe_property):
                    misc = Misc()
                    self.nodes_to_object(misc_node, misc)
                    recipe.miscs.append(misc)

            elif tag_name == "style":
                style = Style()
                recipe.style = style
                self.nodes_to_object(recipe_property, style)

            elif tag_name == "waters":
                for water_node in list(recipe_property):
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

                for mash_node in list(recipe_property):
                    if to_lower(mash_node.tag) == "mash_steps":
                        for mash_step_node in list(mash_node):
                            mash_step = MashStep()
                            self.nodes_to_object(mash_step_node, mash_step)
                            mash.steps.append(mash_step)
                    else:
                        self.node_to_object(mash_node, mash)

            else:
                self.node_to_object(recipe_property, recipe)

        return recipe
