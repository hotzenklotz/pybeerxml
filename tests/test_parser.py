#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from pybeerxml import Parser, Recipe
from pybeerxml.equipment import Equipment
from pybeerxml.hop import Hop
from xml.etree.ElementTree import Element, SubElement
from math import floor

RECIPE_PATH = os.path.join(os.path.dirname(__file__), "Simcoe IPA.xml")
RECIPE_PATH_2 = os.path.join(os.path.dirname(__file__), "Oatmeal Stout.xml")
RECIPE_PATH_3 = os.path.join(os.path.dirname(__file__), "CoffeeStout.xml")

class TestParser:

    def test_parse_recipe(self):

        recipe_parser = Parser()
        recipes = recipe_parser.parse(RECIPE_PATH)

        "should have at least one recipe"
        assert(len(recipes) > 0)

        recipe = recipes[0]

        "should be of type Recipe"
        assert(type(recipe) is Recipe)

        "should have the correct amount of ingredients"
        assert(len(recipe.hops) == 3)
        assert(len(recipe.yeasts) == 1)
        assert(len(recipe.fermentables) == 2)

        "should have mashing steps"
        # TODO

        "should have the correctly calculated properties"
        assert(round(recipe.og, 4) == 1.0338)
        assert(round(recipe.og_plato, 4) == 8.4815)
        assert(round(recipe.fg, 4) == 1.0047)
        assert(round(recipe.fg_plato, 4) == 1.2156)
        assert(floor(recipe.ibu) == 99)
        assert(round(recipe.abv, 2) == 3.84)

        "should have the correct recipe metadata"
        assert(recipe.name == "Simcoe IPA")
        assert(recipe.brewer == "Tom Herold")
        assert(recipe.efficiency == 76.0)
        assert(recipe.batch_size == 14.9902306488)
        assert(recipe.boil_time == 30.0)
        assert(round(recipe.color, 2) == 6.27)

        "should have the correct style metadata"
        assert(recipe.style.name == "American IPA")


    def test_parse_recipe_2(self):

        recipe_parser = Parser()
        recipes = recipe_parser.parse(RECIPE_PATH_2)

        "should have at least one recipe"
        assert(len(recipes) > 0)

        recipe = recipes[0]

        "should be of type Recipe"
        assert(type(recipe) is Recipe)

        "should have the correct amount of ingredients"
        assert(len(recipe.hops) == 1)
        assert(len(recipe.yeasts) == 1)
        assert(len(recipe.fermentables) == 5)

        "should have mashing steps"
        assert(len(recipe.mash.steps) == 2)
        assert(recipe.mash.steps[0].name == "Mash step")
        assert(recipe.mash.steps[0].step_time == 60)
        assert(recipe.mash.steps[0].step_temp == 68)

        "should have the correctly calculated properties"
        assert(round(recipe.og, 4) == 1.0556)
        assert(round(recipe.og_plato, 4) == 13.7108)
        assert(round(recipe.fg, 4) == 1.0139)
        assert(round(recipe.fg_plato, 4) == 3.5467)
        assert(floor(recipe.ibu) == 32)
        assert(round(recipe.abv, 2) == 5.47)

        "should have the correct recipe metadata"
        assert(recipe.name == "Oatmeal Stout no. 1")
        assert(recipe.brewer == "Niels Kjøller") # Python 2 Problem?
        assert(recipe.efficiency == 75.0)
        assert(recipe.batch_size == 25)
        assert(recipe.ibu == 32.21660448470247)
        assert(round(recipe.color, 2) == 40.16)

        "should have the correct style metadata"
        assert(recipe.style.name == "Oatmeal Stout")

        "should have misc ingredients"
        assert(len(recipe.miscs) == 1)
        assert(recipe.miscs[0].name == "Protafloc")
        assert(recipe.miscs[0].use == "Boil")
        assert(recipe.miscs[0].use_for == None)
        assert(recipe.miscs[0].amount == 0.0016)
        assert(recipe.miscs[0].amount_is_weight == True)
        assert(recipe.miscs[0].time == 15)
        assert(recipe.miscs[0].notes == "Half a tablet @ 15 minutes")

    def test_parse_recipe_3(self):

        recipe_parser = Parser()
        recipes = recipe_parser.parse(RECIPE_PATH_3)

        "should have at least one recipe"
        assert(len(recipes) > 0)

        recipe = recipes[0]

        "should be of type Recipe"
        assert(type(recipe) is Recipe)

        "should have the correct amount of ingredients"
        assert(len(recipe.hops) == 2)
        assert(len(recipe.yeasts) == 1)
        assert(len(recipe.fermentables) == 4)

        "should have mashing steps"
        assert(len(recipe.mash.steps) == 2)
        assert(recipe.mash.steps[0].name == "Conversion")
        assert(recipe.mash.steps[0].step_time == 60)
        assert(recipe.mash.steps[0].step_temp == 66.66666667)

        "should have the correctly calculated properties"
        assert(round(recipe.og, 4) == 1.0594)
        assert(round(recipe.og_plato, 4) == 14.6092)
        assert(round(recipe.fg, 4) == 1.0184)
        assert(round(recipe.fg_plato, 4) == 4.684)
        assert(floor(recipe.ibu) == 25)
        assert(round(recipe.abv, 2) == 5.35)

        "should have the correct recipe metadata"
        assert(recipe.name == "Coffee Stout")
        assert(recipe.brewer == "https://github.com/jwjulien")
        assert(recipe.efficiency == 70.0)
        assert(recipe.batch_size == 20.82)
        assert(round(recipe.ibu, 2) == 25.97)
        assert(round(recipe.color, 2) == 35.01)
        assert (recipe.version == 1)
        assert (recipe.type == "All Grain")
        assert (recipe.asst_brewer == "Brewtarget: free beer software")
        assert (recipe.boil_size == 25.552)
        assert (recipe.notes == "Recipe Notes")
        assert (recipe.taste_notes == "Taste Notes")
        assert (recipe.taste_rating == 42)
        assert (recipe.fermentation_stages == 1)
        assert (recipe.date == "3 Dec 04")
        assert (recipe.carbonation == 2.1)
        assert (recipe.forced_carbonation == False)
        assert (recipe.priming_sugar_name == "Honey")
        assert (recipe.carbonation_temp == 20.0)
        assert (recipe.priming_sugar_equiv == 1.1)
        assert (recipe.keg_priming_factor == 1.2)
        assert (recipe.est_og == 1.049)
        assert (recipe.est_fg == 1.015)
        assert (recipe.est_color == 3.1)
        assert (recipe.ibu_method == "Tinseth")
        assert (recipe.est_abv == 6.23)
        assert (recipe.actual_efficiency == 65.1)
        assert (recipe.calories == "180 Cal/pint")
        assert (recipe.carbonation_used == "50g corn sugar")

        "should have the correct style metadata"
        assert(recipe.style.name == "Dry Stout")

        "should have misc ingredients"
        assert(len(recipe.miscs) == 1)
        assert(recipe.miscs[0].name == "Coffee, Dark Roast")
        assert(recipe.miscs[0].use == "Boil")
        assert(recipe.miscs[0].use_for == "Adding coffee notes.")
        assert(recipe.miscs[0].amount == 0.11339809)
        assert(recipe.miscs[0].amount_is_weight == True)
        assert(recipe.miscs[0].time == 0)
        assert(recipe.miscs[0].notes == "Use a coarse grind, add at flameout, steep 20 minutes.")

        "should have equipments"
        assert(isinstance(recipe.equipment, Equipment))
        assert(recipe.equipment.name == "5.5 gal - All Grain - 10 gal Igloo Cooler")
        assert(recipe.equipment.version == 1)
        assert(recipe.equipment.boil_size == 25.552)
        assert(recipe.equipment.batch_size == 20.82)
        assert(recipe.equipment.tun_volume == 37.854)
        assert(recipe.equipment.tun_weight == 4.082)
        assert(recipe.equipment.tun_specific_heat == 0.3)
        assert(recipe.equipment.top_up_water == 0.1)
        assert(recipe.equipment.trub_chiller_loss == 1.893)
        assert(recipe.equipment.evap_rate == 13.63592699)
        assert(recipe.equipment.boil_time == 60.0)
        assert(recipe.equipment.calc_boil_volume == True)
        assert(recipe.equipment.lauter_deadspace == 0.2)
        assert(recipe.equipment.top_up_kettle == 0.4)
        assert(recipe.equipment.hop_utilization == 100.0)
        assert(recipe.equipment.notes == "Equipment notes")


    def test_node_to_object(self):
        "test XML node parsing to Python object"

        node = Element("hop")
        SubElement(node, "name").text = "Simcoe"
        SubElement(node, "alpha").text = 13
        SubElement(node, "amount").text = 0.5
        SubElement(node, "use").text = "boil"
        SubElement(node, "time").text = 30

        test_hop = Hop()

        recipe_parser = Parser()
        recipe_parser.nodes_to_object(node, test_hop)

        assert(test_hop.name == "Simcoe")
        assert(test_hop.alpha == 13)
        assert(test_hop.amount == 0.5)
        assert(test_hop.use == "boil")
        assert(test_hop.time == 30)


    def test_to_lower(self):

        recipe_parser = Parser()
        assert(recipe_parser.to_lower("MASH") == "mash")
        assert(recipe_parser.to_lower("") == "")
        assert(recipe_parser.to_lower(10) == "")
        assert(recipe_parser.to_lower(None) == "")
