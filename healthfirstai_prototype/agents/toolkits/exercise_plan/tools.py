"""Exercise Agent

This module contains the tools for the exercise agent.

"""
from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool

from .utils import edit_workout_schedule_json, get_cached_schedule_json

from .schemas import WorkoutScheduleInput, EditWorkoutScheduleInput
from healthfirstai_prototype.enums.openai_enums import ModelName

from healthfirstai_prototype.utils import get_model

llm = get_model(ModelName.gpt_3_5_turbo)


class WorkoutScheduleTool(BaseTool):
    """
    Params:
        user_id: User ID of the user

    Returns:
        The user's workout schedule
    """

    name = "get_user_workout_schedule"
    description = """
        Should be used whenever you need to get information about the user's workout schedule or exercise plan
        You should pass the user id.
        """
    args_schema: Type[BaseModel] = WorkoutScheduleInput

    def _run(
        self,
        user_id: int,
    ):
        return get_cached_schedule_json(user_id)

    def _arun(
        self,
        user_id: int,
    ):
        raise NotImplementedError("get_user_workout_schedule does not support async")


# NOTE: This tool is currently not being used because we cannot extract workouts yet
class EditWorkoutScheduleTool(BaseTool):
    """
    Edit the user's workout schedule and update redis cache.
    """

    name = "edit_workout_schedule"
    description = """
        Useful when you need to make changes to the user's workout schedule
        You should pass the user input
        You should also pass the user id.
        """
    args_schema: Type[BaseModel] = EditWorkoutScheduleInput

    def _run(
        self,
        agent_input: str,
        user_id: int,
    ):
        return edit_workout_schedule_json(agent_input, user_id)

    def _arun(
        self,
        agent_input: str,
        user_id: int,
    ):
        raise NotImplementedError("edit_workout_schedule does not support async")
