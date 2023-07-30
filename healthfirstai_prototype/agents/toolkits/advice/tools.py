"""Advice Agent
this agent is created for a number of goals/functions. the primary goal for this file is to provide a way to process user queries which require
information about nutrition and exercise. so, this is more of a knowledge base/advice providing agent.

1. to provide a way to search through the nutrition knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)
2. to provide a gateway for the user to search through the internet (SerpAPI) for nutrition/exercise information 
3. get user's personal information NOTE: this function is not used yet
"""
from langchain.utilities import GoogleSerperAPIWrapper
from .chains import (
    load_chain,
    query_based_similarity_search,
)
from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from healthfirstai_prototype.enums.meal_enums import MealNames

from .schemas import (
    BreakfastInput,
    LunchInput,
    DinnerInput,
    DietPlanInput,
    EditDietPlanInput,
    EditBreakfastInput,
    EditLunchInput,
    EditDinnerInput,
)
from .utils import (
    edit_entire_diet_plan,
    edit_meal,
    get_meal,
    get_diet_plan,
)


def kb_vector_search(query: str) -> str:
    """
    This function is used to load the chain and sets it up for the agent to use

    Params:
        query (str) : The user's query / question

    Returns:
        The response from the LLM chain object
    """
    chain = load_chain()
    return query_based_similarity_search(query, chain)


def serp_api_search(query: str) -> str:
    """
    This function is used to search through the internet (SerpAPI)
    for nutrition/exercise information in case it doesn't require further clarification,
    but a simple univocal answer.

    Params:
        query (str) : The user's query / question

    Returns:
        The response from the SerpAPI's query to Google
    """
    search = GoogleSerperAPIWrapper()
    return search.run(query)



class BreakfastTool(BaseTool):
    """
    Retrieve breakfast details from the user's diet plan in the database.

    Parameters:
        user_id (int): The ID of the user.
        include_ingredients (bool): Whether to include breakfast ingredients in the response.
        include_nutrients (bool): Whether to include the nutrients of the breakfast in the response.

    Returns:
        user_json (dict): A dictionary containing the details of the user's breakfast.
    """

    name = "get_breakfast"
    description = """
        Useful when you want to view details of the user's breakfast as it is in their diet plan.
        You should enter the user id.
        You choose whether to include the breakfast ingredients in the breakfast description.
        You choose whether to include the nutrients (macro and micro) of breakfast in the breakfast description.
        """
    args_schema: Type[BaseModel] = BreakfastInput

    def _run(
        self,
        user_id: int,
        include_ingredients: bool,
        include_nutrients: bool,
    ):
        return get_meal(
            user_id,
            include_ingredients,
            include_nutrients,
            MealNames.breakfast,
            cached=True,
        )

    def _arun(
        self,
        user_id: int,
        include_ingredients: bool,
        include_nutrients: bool,
    ):
        raise NotImplementedError("get_lunch does not support async")
