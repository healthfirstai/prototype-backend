from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from datetime import datetime, timedelta
from healthfirstai_prototype.nutrition_utils import (
    get_user_info_dict,
    get_user_meal_plans_as_json,
    get_user_info_for_json_agent,
    get_cached_plan_json,
)
from healthfirstai_prototype.util_models import MealNames
from healthfirstai_prototype.nutrition_chains import run_edit_json_chain
from healthfirstai_prototype.database import SessionLocal
import json

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
