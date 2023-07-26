from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Cohere
from langchain.vectorstores import FAISS
import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""
SERPER_API_KEY = os.getenv("SERPER_API_KEY") or ""


def load_chain(chain_type: str = "map_reduce") -> BaseCombineDocumentsChain:
    """
    This function is loading the chain and sets it up for the agent to use

    Params:
        chain_type (str, optional) : The type of chain to use

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


def query_based_similarity_search(
    query: str, docsearch: FAISS, chain: BaseCombineDocumentsChain
) -> str:
    """
    This function is used to search through the knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)

    Params:
        query (str) : The user's query / question
        docsearch (FAISS) : FAISS wrapper from raw documents to search from based on the similarity search algos
        chain (BaseCombineDocumentsChain) : The LLM chain object

    Returns:
        The response from the LLM chain object
    """
    docs = docsearch.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return response
