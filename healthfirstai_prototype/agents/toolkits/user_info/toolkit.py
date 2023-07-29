"""User Info Toolkit Object

Toolkit object for user related tools

"""
from typing import List
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool

from .tools import GetUserInfoTool


class UserInfoToolkit(BaseToolkit):
    """User Info Toolkit

    Methods:
        get_tools: Get the tools in the toolkit.
    """

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            GetUserInfoTool(),
        ]
