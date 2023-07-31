"""Advice Agent
this agent is created for a number of goals/functions. the primary goal for this file is to provide a way to process user queries which require
information about nutrition and exercise. so, this is more of a knowledge base/advice providing agent.

1. to provide a way to search through the nutrition knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)
2. to provide a gateway for the user to search through the internet (SerpAPI) for nutrition/exercise information 
3. get user's personal information NOTE: this function is not used yet
"""
from typing import Type
from pydantic import BaseModel
from langchain.tools import BaseTool

from healthfirstai_prototype.agents.toolkits.advice.utils import (
    knowledge_base_search,
    search_internet,
)

from .schemas import KnowledgeBaseSearchInput, InternetSearchInput


class KnowledgeBaseSearchTool(BaseTool):
    """
    This tool is used to search through a knowledge base full of nutrition and exercise information

    Params:
        query (str) : The user's query / question

    Returns:
        The response from the LLM chain object
    """

    name = "knowledge_base_search"
    description = """
        Useful when the user asks questions related to sports and exercise nutrition, specifically endurance training
        You should pass the user's query
        """
    args_schema: Type[BaseModel] = KnowledgeBaseSearchInput

    def _run(
        self,
        query: str,
    ):
        return knowledge_base_search(query)

    def _arun(
        self,
        query: str,
    ):
        raise NotImplementedError("knowledge_base_search does not support async")


class InternetSearchTool(BaseTool):
    """
    This function is used to search through the internet (SerpAPI)
    for nutrition/exercise information in case it doesn't require further clarification,
    but a simple univocal answer.

    Params:
        query (str) : The user's query / question

    Returns:
        The response from the SerpAPI's query to Google
    """

    name = "search_internet"
    description = """
        Should be used when whenever the user wants to see pricing information for a food item
        You should pass the user's query to this tool and it will return
        """
    # description = """
    #     Should be used when the user's query is related to general nutrition topics such as food, calories, vitamins, minerals, etc.
    #     Should be used when the user's query is related to general exercise topics such as lifting weights, running, etc.
    #     You should pass the user's query to this tool and it will return
    #     """
    args_schema: Type[BaseModel] = InternetSearchInput

    def _run(
        self,
        query: str,
    ):
        return search_internet(query)

    def _arun(
        self,
        query: str,
    ):
        raise NotImplementedError("search_internet does not support async")
