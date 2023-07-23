from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from datetime import datetime, timedelta
from healthfirstai_prototype.nutrition_utils import (
    get_user_info_dict,
    get_user_meal_plans_as_json,
    get_user_info_for_json_agent,
)
from healthfirstai_prototype.nutrition_chains import init_edit_json_chain


def get_user_info(user_id: int):
    """
    Given a user ID, query the database and return the user's information.
    """
    return get_user_info_for_json_agent(user_id)


class UserInfoInput(BaseModel):
    """
    Inputs for get_user_info
    """

    user_id: int = Field(description="User ID of the user")


class UserInfoTool(BaseTool):
    name = "get_user_info"
    description = """
        Useful when you want to check the user goal information.
        You should enter the user id.
        """
    args_schema: Type[BaseModel] = UserInfoInput

    def _run(self, user_id: int):
        return get_user_info(user_id)

    def _arun(self, user_id: int):
        raise NotImplementedError("get_user_info does not support async")


def get_diet_plan(user_id: int, include_ingredients: bool):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    return get_user_meal_plans_as_json(user_id, include_ingredients)


class DietPlanInput(BaseModel):
    """
    Inputs for get_diet_plan
    """

    user_id: int = Field(description="User ID of the user")
    include_ingredients: bool = Field(
        description="Whether to include the ingredients in the meal plan"
    )


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

    def _arun(self, user_id: int, include_ingredients: bool):
        raise NotImplementedError("get_diet_plan does not support async")


def edit_diet_plan(agent_input: str, user_diet_plan_json: str):
    """
    Takes a user diet plan and edits it based on the agent input
    """
    return init_edit_json_chain().predict(
        agent_input=agent_input,
        user_diet_plan_json=user_diet_plan_json,
    )


class EditDietPlanInput(BaseModel):
    """
    Inputs for edit_diet_plan
    """

    agent_input: str = Field(description="The input from the user")
    user_diet_plan: str = Field(description="JSON string of the user's diet plan")


class EditDietPlanTool(BaseTool):
    name = "edit_diet_plan"
    description = """
        Useful when you need to make changes to the user's diet plan.
        You should pass the user input
        You should add the JSON string of the user plan
        """
    args_schema: Type[BaseModel] = EditDietPlanInput

    def _run(self, agent_input: str, user_diet_plan: str):
        return edit_diet_plan(agent_input, user_diet_plan)

    def _arun(self, agent_input: str, user_diet_plan: str):
        raise NotImplementedError("edit_diet_plan does not support async")
