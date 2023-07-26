from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Cohere
from langchain.vectorstores import FAISS
from langchain.utilities import GoogleSerperAPIWrapper
from healthfirstai_prototype.advice_tools import load_prerequisites_for_vector_search
from healthfirstai_prototype.advice_agent import COHERE_API_KEY
from healthfirstai_prototype.advice_agent import SERPER_API_KEY


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


def faiss_vector_search(query: str, reader) -> str:
    """
    This function is used to load the chain and sets it up for the agent to use

    Params:
        query (str) : The user's query / question
        reader (PdfReader) : The PDF file in the PDFReader format

    Returns:
        The response from the LLM chain object
    """
    chain = load_chain()
    docsearch = load_prerequisites_for_vector_search(reader)
    response = query_based_similarity_search(query, docsearch, chain)
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
