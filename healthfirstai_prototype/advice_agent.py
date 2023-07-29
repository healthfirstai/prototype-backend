import os
from dotenv import load_dotenv
from langchain.utilities import GoogleSerperAPIWrapper
from healthfirstai_prototype.advice_chains import (
    load_chain,
    query_based_similarity_search,
)

"""
this agent is created for a number of goals/functions. the primary goal for this file is to provide a way to process user queries which require
information about nutrition and exercise. so, this is more of a knowledge base/advice providing agent.

1. to provide a way to search through the nutrition knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)
2. to provide a gateway for the user to search through the internet (SerpAPI) for nutrition/exercise information 
3. get user's personal information NOTE: this function is not used yet
"""

# Load env file
load_dotenv()

# Load API keys
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""
SERPER_API_KEY = os.getenv("SERPER_API_KEY") or ""
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or ""


def kb_vector_search(query: str) -> str:
    """
    This function is used to load the chain and sets it up for the agent to use

    Params:
        query (str) : The user's query / question

    Returns:
        The response from the LLM chain object
    """
    chain = load_chain()
    response = query_based_similarity_search(query, chain)
    return response


def serp_api_search(query: str) -> str:
    """
    This function is used to search through the internet (SerpAPI)
    for nutrition/exercise information in case it doesn't require further clarification,
    but a simple univocal answer.

    Params:
        query (str) : The user's query / question

    Returns:
        The response from the SerpAPI's query to Google
    """
    search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
    response = search.run(query)
    return response


# testing the functions and putting them up together
def main():
    query = "How many hours a day should I have?"
    google_search_results = serp_api_search(query)
    kb_search_results = kb_vector_search(query)

    print("--------------------------------------")
    print("Query: ", query)
    print("--------------------------------------")
    print("KB response: ", kb_search_results)
    print("--------------------------------------")
    print("Google Search: ", google_search_results)
    print("--------------------------------------")


if __name__ == "__main__":
    main()
