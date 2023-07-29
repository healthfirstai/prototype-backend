import os
from langchain.llms import Cohere
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.question_answering import load_qa_chain
from .advice_tools import query_pinecone_index

COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""


def load_chain(chain_type: str = "stuff") -> BaseCombineDocumentsChain:
    """
    This function is loading the chain and sets it up for the agent to use

    Params:
        chain_type (str, optional) : The type of chain to use ("stuff" or "map_reduce")

    Returns:
        The LLM chain object
    """
    chain = load_qa_chain(
        Cohere(cohere_api_key=COHERE_API_KEY, verbose=False),  # type: ignore
        chain_type=chain_type,
        # Setting verbose to True will print out the internal state of the Chain object while it is running.
        verbose=True,
    )
    return chain


def query_based_similarity_search(query: str, chain: BaseCombineDocumentsChain) -> str:
    """
    This function is used to search through the knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)

    Params:
        query (str): The user's query / question
        chain (BaseCombineDocumentsChain) : The LLM chain object

    Returns:
        The response from the LLM chain object
    """
    docs = query_pinecone_index(query)
    response = chain.run(input_documents=docs, question=query)
    return response
