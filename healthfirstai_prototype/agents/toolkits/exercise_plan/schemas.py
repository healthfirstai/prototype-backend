from pydantic import BaseModel, Field


class WorkoutScheduleInput(BaseModel):
    """
    Inputs for get_workout_schedule

    Attributes:
        user_id: User ID of the user
    """

    user_id: int = Field(description="User ID of the user")
    # TODO: Add more fields like include_descriptions, include_links, etc


class EditWorkoutScheduleInput(BaseModel):
    """
    Inputs for edit_workout_schedule

    Attributes:
        user_id: User ID of the user
    """

    agent_input: str = Field(description="The input from the user")
    user_id: int = Field(description="User ID of the user")
