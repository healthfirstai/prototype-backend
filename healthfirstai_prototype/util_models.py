from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    """
    Enum for model names
    """
    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_3_5_turbo_0613 = "gpt-3.5-turbo-0613"
    text_davinci_003 = "text-davinci-003"
    text_embedding_ada_002 = "text-embedding-ada-002"

class MealNames(str, Enum):
    """
    Enum for model names
    """
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    snack = "Snack"
    drink = "Drink"

class UserInput(BaseModel):
    user_input: str = ""
    verbose: bool = False
