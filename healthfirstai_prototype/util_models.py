"""Utility Models

This file contains the utility models used project-wide.

"""
from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    """
    Enum for model names

    Attributes:
        gpt_3_5_turbo: GPT-3 5B model
        gpt_3_5_turbo_0613: GPT-3 5B model with 0613 prompt
        text_davinci_003: Davinci model with 003 prompt
        text_embedding_ada_002: Ada model with 002 prompt
    """

    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_3_5_turbo_0613 = "gpt-3.5-turbo-0613"
    text_davinci_003 = "text-davinci-003"
    text_embedding_ada_002 = "text-embedding-ada-002"


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


class UserInput(BaseModel):
    user_input: str = ""
    verbose: bool = False
