from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from healthfirstai_prototype.util_models import MealNames

from healthfirstai_prototype.nutrition_tool_models import (
    UserInfoInput,
    BreakfastInput,
    LunchInput,
    DinnerInput,
    DietPlanInput,
    EditDietPlanInput,
)
from healthfirstai_prototype.nutrition_tool_service import (
    edit_diet_plan,
    get_meal,
    get_diet_plan,
    get_user_info,
)


class UserInfoTool(BaseTool):
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
    args_schema: Type[BaseModel] = UserInfoInput

    def _run(self, user_id: int):
        return get_user_info(user_id)

    def _arun(self, user_id: int):
        raise NotImplementedError("get_user_info does not support async")


class BreakfastTool(BaseTool):
    """
    Retrieve breakfast details from the user's diet plan in the database.

    Parameters:
        user_id (int): The ID of the user.
        include_ingredients (bool): Whether to include breakfast ingredients in the response.
        include_nutrients (bool): Whether to include the nutrients of the breakfast in the response.

    Returns:
        dict: A dictionary containing the details of the user's breakfast.
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
        dict: A dictionary containing the details of the user's lunch.
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
        dict: A dictionary containing the details of the user's dinner.
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
        dict: A dictionary containing the details of the user's meal plan.
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
    Edit the user's diet plan in the database.

    Parameters:
        agent_input (str): The user's input text for making changes to the diet plan.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the updated details of the user's diet plan.
    """

    name = "edit_diet_plan"
    description = """
        Useful when you need to make changes to the user's diet plan.
        You should pass the user input
        You should also pass the user id.
        """
    args_schema: Type[BaseModel] = EditDietPlanInput

    def _run(self, agent_input: str, user_id: int):
        return edit_diet_plan(agent_input, user_id)

    def _arun(
        self,
        agent_input: str,
        user_id: int,
    ):
        raise NotImplementedError("edit_diet_plan does not support async")


# TODO: Add edit_breakfast, edit_lunch, edit_dinner

# TODO: Change EditDietPlanTool to EditEntireDietPlanTool to specify that this should only be used when the user wants to make a change to their diet plan that affects all meals.
