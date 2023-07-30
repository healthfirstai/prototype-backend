"""Advice Toolkit Object

Toolkit object for nutrition and exercise advice related tasks.

"""
from typing import List, Optional
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool

from healthfirstai_prototype.models.data_models import User
from .tools import KnowledgeBaseSearchTool, InternetSearchTool


class AdviceToolkit(BaseToolkit):
    """Health and Fitness Advice Toolkit

    Parameters:
        user_info (User): The user's information.

    Methods:
        get_tools: Get the tools in the toolkit.
    """

    user_info: Optional[User] = None

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            # KnowledgeBaseSearchTool(),
            InternetSearchTool(),
        ]
