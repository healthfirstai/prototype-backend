from pydantic import BaseModel, Field

class FindSimilarFoodsInput(BaseModel):
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
