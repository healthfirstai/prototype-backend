from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool

from healthfirstai_prototype.nutrition_tool_models import (
    UserInfoInput)
from healthfirstai_prototype.nutrition_tool_service import get_user_info


class GetUserInfoTool(BaseTool):
    """
    Retrieve user information from the database.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the personal and goal information of the user.
    """

    name = "get_user_info"
    description = """
        Useful when you want to check the user personal information and goal information.
        You should enter the user id.
        """
    args_schema: Type[BaseModel] = UserInfoInput

    def _run(self, user_id: int):
        return get_user_info(user_id)

    def _arun(self, user_id: int):
        raise NotImplementedError("get_user_info does not support async")

