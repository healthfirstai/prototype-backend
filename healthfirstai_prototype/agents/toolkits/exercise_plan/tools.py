"""Exercise Agent

This module contains the tools for the exercise agent.

"""
from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool

from .utils import edit_workout_schedule_json, get_cached_schedule_json

from .schemas import WorkoutScheduleInput, EditWorkoutScheduleInput, TodaysScheduleInput
from healthfirstai_prototype.enums.exercise_enums import DaysOfTheWeek


class TodaysScheduleTool(BaseTool):
    """
    Params:
        user_id: User ID of the user

    Returns:
        The user's workout schedule
    """

    # TODO: Change these tool names project wide to remove underscores
    name = "get_todays_workout_schedule"
    description = """
        Should be used whenever you need to get information about the user's workout schedule or exercise plan for today
        You should pass the user id.
        """
    args_schema: Type[BaseModel] = TodaysScheduleInput

    def _run(
        self,
        user_id: int,
    ):
        return get_cached_schedule_json(
            user_id,
            include_descriptions=False,
            day_of_the_week=DaysOfTheWeek.today,
        )

    def _arun(
        self,
        user_id: int,
    ):
        raise NotImplementedError("get_user_workout_schedule does not support async")


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
        return get_cached_schedule_json(
            user_id,
            include_descriptions=False,
            day_of_the_week=None,
        )

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
