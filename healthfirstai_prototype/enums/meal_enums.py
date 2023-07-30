"""Meal Enums

This file contains the enums used for meals.

"""
from enum import Enum


class MealNames(str, Enum):
    """
    Enum for model names

    Attributes:
        breakfast: Breakfast
        lunch: Lunch
        dinner: Dinner
        snack: Snack
        drink: Drink
        all: All
    """

    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    snack = "Snack"
    drink = "Drink"
    all = ""


class MealChoice(str, Enum):
    """
    Enum for abbreviated meal choice

    Attributes:
        breakfast: Breakfast
        lunch: Lunch
        dinner: Dinner
        snack: Snack
        drink: Drink
        all: All
    """

    breakfast = "b"
    lunch = "l"
    dinner = "d"
    snack = "s"
    all = ""
