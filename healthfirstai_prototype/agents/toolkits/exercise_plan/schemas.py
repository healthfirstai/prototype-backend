from pydantic import BaseModel, Field


class WorkoutScheduleInput(BaseModel):
    """
    Inputs for get_workout_schedule

    Attributes:
        user_id: User ID of the user
    """

    user_id: int = Field(description="User ID of the user")


class EditWorkoutScheduleInput(BaseModel):
    """
    Inputs for edit_workout_schedule

    Attributes:
        user_id: User ID of the user
    """

    user_id: int = Field(description="User ID of the user")