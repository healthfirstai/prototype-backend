"""Test Exercise Utils

Unit tests for the advice utils module

"""

from healthfirstai_prototype.agents.toolkits.exercise_plan.utils import (
    get_cached_schedule_json,
)
from healthfirstai_prototype.enums.exercise_enums import DaysOfTheWeek
import json


def test_get_all_workouts():
    """
    Test that get_cached_schedule_json returns all the workouts in the week
    """
    output = get_cached_schedule_json(1, include_descriptions=True)
    output_dict = json.loads(output)
    assert all(
        boolean is True
        for boolean in [(k in list(DaysOfTheWeek)) for k in output_dict.keys()]
    )


def test_get_all_workouts_without_description():
    """
    Test that get_cached_schedule_json returns all the workouts without description when include_descriptions is False
    """
    output = get_cached_schedule_json(
        1, include_descriptions=False, day_of_the_week=DaysOfTheWeek.monday
    )
    output_dict = json.loads(output)
    assert all(
        desc is None
        for desc in (
            exercise.pop("description", None) for exercise in output_dict["exercises"]
        )
    )
