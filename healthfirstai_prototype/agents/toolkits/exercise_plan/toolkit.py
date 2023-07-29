from typing import List, Optional
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from .tools import (
    WorkoutScheduleTool,
    EditWorkoutScheduleTool,
)
# NOTE: Same implementation as diet_plan/toolkit.py
# check comments there

from healthfirstai_prototype.models.data_models import User


class WorkoutScheduleToolKit(BaseToolkit):
    """Diet Plan Toolkit

    Parameters:
        user_info (User): The user's information.

    Methods:
        get_tools: Get the tools in the toolkit.
    """

    user_info: Optional[User] = None

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [WorkoutScheduleTool(), EditWorkoutScheduleTool()]
