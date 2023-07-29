"""Diet Plan Schemas

This module contains the logic for the nutrition feature.

Todo:
    * Move some of this logic out of this file and into a general conttoller file. It has nothing to do with the agent itself.
"""
from pydantic import BaseModel, Field


class UserInfoInput(BaseModel):
    """
    Inputs for get_user_info

    Attributes:
        user_id: User ID of the user
    """

    user_id: int = Field(description="User ID of the user")


class DinnerInput(BaseModel):
    """
    Inputs for get_dinner

    Attributes:
        user_id: User ID of the user
        include_ingredients: Whether to include the ingredients in the dinner description
        include_nutrients: Whether to include nutrient information about dinner in the breakfast description
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

    Attributes:
        user_id: User ID of the user
        include_ingredients: Whether to include the ingredients in the lunch description
        include_nutrients: Whether to include nutrient information about lunch in the breakfast description
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

    Attributes:
        user_id: User ID of the user
        include_ingredients: Whether to include the ingredients in the breakfast description
        include_nutrients: Whether to include nutrient information about breakfast in the breakfast description
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

    Attributes:
        user_id: User ID of the user
        include_ingredients: Whether to include the ingredients in the meal plan
    """

    user_id: int = Field(description="User ID of the user")
    include_ingredients: bool = Field(
        description="Whether to include the ingredients in the meal plan"
    )


class EditDietPlanInput(BaseModel):
    """
    Inputs for edit_entire_diet_plan

    Attributes:
        agent_input: The input from the user
        user_id: User ID of the user
    """

    agent_input: str = Field(description="The input from the user")
    user_id: int = Field(description="User ID of the user")


class EditBreakfastInput(BaseModel):
    """
    Inputs for edit_entire_diet_plan

    Attributes:
        agent_input: The input from the user
        user_id: User ID of the user
    """

    agent_input: str = Field(description="The input from the user")
    user_id: int = Field(description="User ID of the user")
    edit_ingredients: bool = Field(
        description="Whether to edit the breakfast ingredients"
    )


class EditLunchInput(BaseModel):
    """
    Inputs for edit_entire_diet_plan

    Attributes:
        agent_input: The input from the user
        user_id: User ID of the user
        edit_ingredients: Whether to edit the lunch ingredients
    """

    agent_input: str = Field(description="The input from the user")
    user_id: int = Field(description="User ID of the user")
    edit_ingredients: bool = Field(description="Whether to edit the lunch ingredients")


class EditDinnerInput(BaseModel):
    """
    Inputs for edit_entire_diet_plan

    Attributes:
        agent_input: The input from the user
        user_id: User ID of the user
        edit_ingredients: Whether to edit the dinner ingredients
    """

    agent_input: str = Field(description="The input from the user")
    user_id: int = Field(description="User ID of the user")
    edit_ingredients: bool = Field(description="Whether to edit the dinner ingredients")
