from abc import ABC
from typing import Type

from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from healthfirstai_prototype.agents.toolkits.exercise_plan.schemas import WorkoutScheduleInput
from healthfirstai_prototype.models.database import OPENAI_API_KEY

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

class WorkoutScheduleTool(BaseTool):
    """
    Retrieve the user's workout schedule from the database.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the details of the user's workout schedule.
    """

    name = "get_diet_plan"
    description = """
        Useful when you want to examine the user diet plan.
        You should enter the user id.
        You can also choose whether to include the ingredients in the meal plan.
        """
    args_schema: Type[BaseModel] = WorkoutScheduleInput

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
        dict: A dictionary containing the updated details of the user's diet plan.
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
