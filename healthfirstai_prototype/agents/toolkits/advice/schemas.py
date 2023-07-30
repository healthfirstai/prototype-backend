from pydantic import BaseModel, Field


class KnowledgeBaseSearchInput(BaseModel):
    """
    Inputs for knowledge_base_search

    Attributes:
        query: The user's query / question
    """

    query: str = Field(description="The user's health or fitness related query")


class InternetSearchInput(BaseModel):
    """
    Inputs for internet_search

    Attributes:
        query: The user's query / question
    """

    query: str = Field(description="The user's health or fitness related query")
