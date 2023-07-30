"""Test Advice Utils

Unit tests for the advice utils module

"""

from healthfirstai_prototype.agents.toolkits.advice.utils import (
    query_pinecone_index,
    knowledge_base_search,
    search_internet,
)

def test_query_pinecone_index():
    """
    Test the query_pinecone_index returns a list of documents given a user's
    """
    output = query_pinecone_index("Hello world")
    assert type(output) == list


def test_knowledge_base_search():
    """
    Test that the knowledge_base_search function returns a string and is working
    """
    output = knowledge_base_search("Hello world")
    assert type(output) == str


def test_search_internet():
    """
    Test that the search_internet function returns a string and is working
    """
    output = search_internet("How much does coffee cost?")
    assert type(output) == str
