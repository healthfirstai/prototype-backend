from pydantic import BaseModel, Field


class UserInfoInput(BaseModel):
    """
    Inputs for get_user_info
    """

    user_id: int = Field(description="User ID of the user")


class DinnerInput(BaseModel):
    """
    Inputs for get_dinner
    """

    user_id: int = Field(description="User ID of the user")
    include_ingredients: bool = Field(
        description="Whether to include the ingredients in the dinner description"
    )
    include_nutrients: bool = Field(
        description="Whether to include nutrient information about dinner in the breakfast description"
    )


class LunchInput(BaseModel):
    """
    Inputs for get_lunch
    """

    user_id: int = Field(description="User ID of the user")
    include_ingredients: bool = Field(
        description="Whether to include the ingredients in the lunch description"
    )
    include_nutrients: bool = Field(
        description="Whether to include nutrient information about lunch in the breakfast description"
    )


class BreakfastInput(BaseModel):
    """
    Inputs for get_breakfast
    """

    user_id: int = Field(description="User ID of the user")
    include_ingredients: bool = Field(
        description="Whether to include the ingredients in the breakfast description"
    )
    include_nutrients: bool = Field(
        description="Whether to include nutrient information about breakfast in the breakfast description"
    )


class DietPlanInput(BaseModel):
    """
    Inputs for get_diet_plan
    """

    user_id: int = Field(description="User ID of the user")
    include_ingredients: bool = Field(
        description="Whether to include the ingredients in the meal plan"
    )


class EditDietPlanInput(BaseModel):
    """
    Inputs for edit_diet_plan
    """

    agent_input: str = Field(description="The input from the user")
    user_id: int = Field(description="User ID of the user")
