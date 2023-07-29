from pydantic import BaseModel, Field


class UserInfoInput(BaseModel):
    """
    Inputs for get_user_info

    Attributes:
        user_id: User ID of the user
    """

    user_id: int = Field(description="User ID of the user")
