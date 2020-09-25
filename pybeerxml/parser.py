import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import Union, List

from pybeerxml.recipe import Recipe
from pybeerxml.hop import Hop
from pybeerxml.mash import Mash
from pybeerxml.mash_step import MashStep
from pybeerxml.misc import Misc
from pybeerxml.yeast import Yeast
from pybeerxml.style import Style
from pybeerxml.fermentable import Fermentable
from pybeerxml.utils import to_lower


class Parser:
    def nodes_to_object(
        self,
        nodes: Element,
        beerxml_object: Union[
            Recipe, Mash, Yeast, Fermentable, Hop, Misc, MashStep, Style
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
            Recipe, Mash, Yeast, Fermentable, Hop, Misc, MashStep, Style
        ],
    ):
        "Map a single node to an object's attributes"

        attribute = to_lower(node.tag)

        # Yield is a protected keyword in Python, so let's rename it
        attribute = "_yield" if attribute == "yield" else attribute

        try:
            value_string = node.text or ""
            value = float(value_string)
        except ValueError:
            value = node.text

        try:
            setattr(beerxml_object, attribute, value)
        except AttributeError:
            sys.stderr.write("Attribute {} not supported.".format(attribute))

    def parse(self, xml_file) -> List[Recipe]:
        "Get a list of parsed recipes from BeerXML input"

        recipes = []

        with open(xml_file, "rt") as file:
            tree = ElementTree.parse(file)

        for recipe_node in tree.iter():
            if to_lower(recipe_node.tag) != "recipe":
                continue

            recipe = Recipe()
            recipes.append(recipe)

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
                            self.nodes_to_object(mash_node, mash)

                else:
                    self.node_to_object(recipe_property, recipe)

        return recipes
