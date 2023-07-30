"""Diet Plan Tools

Tools used in agents for the nutrition feature.

"""
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


class BreakfastTool(BaseTool):
    """
    Retrieve breakfast details from the user's diet plan in the database.

    Parameters:
        user_id (int): The ID of the user.
        include_ingredients (bool): Whether to include breakfast ingredients in the response.
        include_nutrients (bool): Whether to include the nutrients of the breakfast in the response.

    Returns:
        str: A dictionary containing the details of the user's breakfast.
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


class LunchTool(BaseTool):
    """
    Retrieve lunch details from the user's diet plan in the database.

    Parameters:
        user_id (int): The ID of the user.
        include_ingredients (bool): Whether to include lunch ingredients in the response.
        include_nutrients (bool): Whether to include the nutrients of the lunch in the response.

    Returns:
        str: A JSON string containing the details of the user's lunch.
    """

    name = "get_lunch"
    description = """
        Useful when you want to view details of the user's lunch as it is in their diet plan.
        You should enter the user id.
        You choose whether to include the lunch ingredients in the lunch description.
        You choose whether to include the nutrients (macro and micro) of lunch in the lunch description.
        """
    args_schema: Type[BaseModel] = LunchInput

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
            MealNames.lunch,
            cached=True,
        )

    def _arun(
        self,
        user_id: int,
        include_ingredients: bool,
        include_nutrients: bool,
    ):
        raise NotImplementedError("get_lunch does not support async")


class DinnerTool(BaseTool):
    """
    Retrieve dinner details from the user's diet plan in the database.

    Parameters:
        user_id (int): The ID of the user.
        include_ingredients (bool): Whether to include dinner ingredients in the response.
        include_nutrients (bool): Whether to include the nutrients of the dinner in the response.

    Returns:
        str: A JSON string containing the details of the user's dinner.
    """

    name = "get_dinner"
    description = """
        Useful when you want to view details of the user's dinner as it is in their diet plan.
        You should enter the user id.
        You choose whether to include the dinner ingredients in the dinner description.
        You choose whether to include the nutrients (macro and micro) of dinner in the dinner description.
        """
    args_schema: Type[BaseModel] = DinnerInput

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
            MealNames.dinner,
            cached=True,
        )

    def _arun(
        self,
        user_id: int,
        include_ingredients: bool,
        include_nutrients: bool,
    ):
        raise NotImplementedError("get_dinner does not support async")


class DietPlanTool(BaseTool):
    """
    Retrieve the user's diet plan from the database.

    Parameters:
        user_id (int): The ID of the user.
        include_ingredients (bool): Whether to include the ingredients in the meal plan.

    Returns:
        str: A JSON string containing the details of the user's meal plan.
    """

    name = "get_diet_plan"
    description = """
        Useful when you want to examine the user diet plan.
        You should enter the user id.
        You can also choose whether to include the ingredients in the meal plan.
        """
    args_schema: Type[BaseModel] = DietPlanInput

    def _run(self, user_id: int, include_ingredients: bool):
        return get_diet_plan(user_id, include_ingredients)

    def _arun(
        self,
        user_id: str,
        include_ingredients: bool,
    ):
        raise NotImplementedError("get_diet_plan does not support async")


class EditDietPlanTool(BaseTool):
    """
    Modify the user's entire diet plan and update the redis cache.

    Parameters:
        agent_input (str): The user's input text for making changes to the diet plan.
        user_id (int): The ID of the user.

    Returns:
        str: A JSON string containing the updated details of the user's diet plan.
    """

    name = "edit_entire_diet_plan"
    description = """
        Useful when you need to make changes to multiple meals or ingredients at a time in the user's diet plan.
        You should pass the user input
        You should also pass the user id.
        """
    args_schema: Type[BaseModel] = EditDietPlanInput

    def _run(self, agent_input: str, user_id: int):
        return edit_entire_diet_plan(agent_input, user_id)

    def _arun(self, agent_input: str, user_id: int):
        raise NotImplementedError("edit_entire_diet_plan does not support async")


class EditBreakfastTool(BaseTool):
    """
    Edit the user's breakfast plan and update the redis cache.

    Parameters:
        agent_input (str): The user's input text for making changes to the breakfast plan.
        user_id (int): The ID of the user.
        edit_ingredients (bool): Whether to edit the ingredients in the breakfast.

    Returns:
        str: A JSON string containing the updated details of the user's breakfast.
    """

    name = "edit_breakfast"
    description = """
        Useful when you need to make changes to the user's breakfast plan
        You should pass the user input
        You should also pass the user id.
        You should decide whether to you need to edit the ingredients content of the the breakfast or just change what is being eaten for breakfast
        """
    args_schema: Type[BaseModel] = EditBreakfastInput

    def _run(self, agent_input: str, user_id: int, edit_ingredients: bool):
        return edit_meal(
            agent_input,
            user_id,
            MealNames.breakfast,
            edit_ingredients,
        )

    def _arun(self, agent_input: str, user_id: int, edit_ingredients: bool):
        raise NotImplementedError("edit_breakfast does not support async")


class EditLunchTool(BaseTool):
    """
    Edit the user's lunch plan and update the redis cache.

    Parameters:
        agent_input (str): The user's input text for making changes to the lunch plan.
        user_id (int): The ID of the user.
        edit_ingredients (bool): Whether to edit the ingredients in the lunch.

    Returns:
        str: A JSON string containing the updated details of the user's lunch.
    """

    name = "edit_lunch"
    description = """
        Useful when you need to make changes to the user's lunch plan
        You should pass the user input
        You should also pass the user id.
        You should decide whether to you need to edit the ingredients content of the the lunch or just change what is being eaten for lunch
        """
    args_schema: Type[BaseModel] = EditLunchInput

    def _run(self, agent_input: str, user_id: int, edit_ingredients: bool):
        return edit_meal(
            agent_input,
            user_id,
            MealNames.lunch,
            edit_ingredients,
        )

    def _arun(self, agent_input: str, user_id: int, edit_ingredients: bool):
        raise NotImplementedError("edit_lunch does not support async")


class EditDinnerTool(BaseTool):
    """
    Edit the user's dinner plan and update the redis cache.

    Parameters:
        agent_input (str): The user's input text for making changes to the dinner plan.
        user_id (int): The ID of the user.
        edit_ingredients (bool): Whether to edit the ingredients in the dinner.

    Returns:
        str: A JSON string containing the updated details of the user's dinner.
    """

    name = "edit_dinner"
    description = """
        Useful when you need to make changes to the user's dinner plan
        You should pass the user input
        You should also pass the user id.
        You should decide whether to you need to edit the ingredients content of the the dinner or just change what is being eaten for dinner
        """
    args_schema: Type[BaseModel] = EditDinnerInput

    def _run(self, agent_input: str, user_id: int, edit_ingredients: bool):
        return edit_meal(
            agent_input,
            user_id,
            MealNames.dinner,
            edit_ingredients,
        )

    def _arun(self, agent_input: str, user_id: int, edit_ingredients: bool):
        raise NotImplementedError("edit_dinner does not support async")
