"""Nutrition Info Tools

Tools used in the nutrition lookup feature

"""
from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from .utils import nutritional_similarity_search
from .schemas import FindSimilarFoodsInput


class FindSimilarFoodsTool(BaseTool):
    """
    Retrieve user information from the database.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the personal and goal information of the user.
    """

    name = "get_user_info"
    description = """
        Useful when you want to check the user personal information and goal information.
        You should enter the user id.
        """
    args_schema: Type[BaseModel] = FindSimilarFoodsInput

    def _run(self, food_name: str, top_k: int):
        return nutritional_similarity_search(food_name, top_k)

    def _arun(self, food_name: str, top_k: int):
        raise NotImplementedError("get_user_info does not support async")


# TODO: When I implement the SQL query tool, consider splitting up the tool by task. So, one of them can be
# I think that it makes sense for me to write a custom LangChain agent
# - Compare foods with basic operators (greater than, less than, approximately equal to)
# - Find similar foods
# - Advanced queries: combine basic operators with nutritional similarity search. Ex:
