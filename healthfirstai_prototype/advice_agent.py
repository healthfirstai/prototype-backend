import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Cohere
from langchain.chains import LLMChain
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain.schema import BaseMessage

# NOTE: Use this class in the future to implement the evaluation techniques
from langchain.evaluation import QAEvalChain

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

# location of the pdf file/files.
path_to_pdf = "../notebooks/pdfs/Sports-And-Exercise-Nutrition.pdf"
reader = PdfReader(path_to_pdf)


def parse_user_info(user_data) -> dict[str, str]:
    """
    this function is used to parse the user's personal information
    :param user_data: the user's personal information
    :return: a dictionary containing the user's personal information
    NOTE: this function is not used yet
    """
    return {
        "height": str(user_data.height),
        "weight": str(user_data.weight),
        "gender": str(user_data.gender),
        "age": str(user_data.age),
        "city_id": str(user_data.city_id),
        "country_id": str(user_data.country_id),
    }


def set_template(
    height: str,
    weight: str,
    gender: str,
    age: str,
    height_unit: str = "cm",
    weight_unit: str = "kg",
    text: str = "This is a default query.",
) -> list[BaseMessage]:
    """
    this function is setting the template for the chat to use given user's personal information
    NOTE: this function is not used yet
    :param height: user's height
    :param weight: user's weight
    :param gender: user's gender
    :param age: user's age
    :param height_unit: user's height unit
    :param weight_unit: user's weight unit
    :return: a list of messages using the formatted prompt
    """
    system_message_template = "You are a helpful nutrition and exercise assistant that takes into the considerations user's height as {user_height}, user weight as {user_weight}, user's gender as {user_gender}, and user's {user_age} to provide a user with answers to their questions. If you don't have a specific answer, just say I don't know, and do not make anything up."
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_message_template
    )

    human_template = text
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    return chat_prompt.format_prompt(
        user_height=height + " " + height_unit,
        user_weight=weight + " " + weight_unit,
        user_gender=gender,
        user_age=age + " years old",
    ).to_messages()


def template_to_assess_search_results(
    google_search_result: str = "",
    faiss_search_result: str = "",
    prompt: str = "",
) -> str:
    """
    this function is used to assess the outputs from the two search engines
    :param google_search_result: the response from the SerpAPI's query to Google
    :param faiss_search_result: the response from the LLM chain object
    :return: a list of messages using the formatted prompt
    """
    system_message_template = """\
    You are a helpful assistant which helps to assess the relevance of the Google search result: {google_search_result}, and the knowledge base search result: {faiss_search_result} regarding the following prompt / question: {prompt}. 
    Please look at both of the search results regarding the prompt I gave you, and return to me that particular result without modifying it. If you think they are both good enough, please return the knowledge base search result, otherwise return the Google search result. 
    Do not make anything up.
    """

    system_message_prompt = PromptTemplate.from_template(system_message_template)

    return system_message_prompt.format(
        google_search_result=google_search_result,
        faiss_search_result=faiss_search_result,
        prompt=prompt,
    )


def run_assessment_chain(prompt_template: str) -> str:
    llm = Cohere(
        cohere_api_key=COHERE_API_KEY,
        temperature=0,
        verbose=False,
        model="command-light",
    )  # type: ignore
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)  # type: ignore
    response = llm_chain.run()
    return response


def collect_raw_text_from_pdf_data(reader: PdfReader) -> str:
    """
    this function is used to collect raw text from the PDF file
    :param reader: the PDF file in the PDFReader format
    :return: raw text collected from PDF file
    """
    raw_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text


def split_text(raw_text: str) -> list[str]:
    """
    this function is used to split the raw text into chunks
    :param raw_text: raw text collected from the PDF file
    :return: a list of text chunks
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    return text_splitter.split_text(raw_text)


# FIXME: think of how this fucntion's output could be stored in Redis DB
def embed_text(texts: list[str]) -> FAISS:
    """
    this function is embedding the text using the Cohere embedding + FAISS library
    :param texts: a list of text chunks
    :return: FAISS wrapper from raw documents
    """
    # Download embeddings from Cohere
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)  # type: ignore
    # Construct FAISS wrapper from raw documents
    docsearch = FAISS.from_texts(texts, embeddings)  # type: ignore

    return docsearch


def load_prerequisites_for_vector_search(reader: PdfReader) -> FAISS:
    """
    this function is used to load the prerequisites for the agent to use
    :param reader: the PDF file in the PDFReader format
    :return: FAISS wrapper from raw documents
    """
    raw_text = collect_raw_text_from_pdf_data(reader)
    texts = split_text(raw_text)
    docsearch = embed_text(texts)
    return docsearch


def load_chain(chain_type: str = "map_reduce") -> BaseCombineDocumentsChain:
    """
    this function is loading the chain and sets it up for the agent to use
    :param chain_type: the type of chain to use
    :return: the LLM chain object
    """
    chain = load_qa_chain(
        Cohere(cohere_api_key=COHERE_API_KEY, verbose=True),  # type: ignore
        chain_type=chain_type,
        # Setting verbose to True will print out some internal states of the Chain object while it is being ran.
        verbose=True,
    )
    return chain


def query_based_similarity_search(
    query: str, docsearch: FAISS, chain: BaseCombineDocumentsChain
) -> str:
    """
    this function is used to search through the knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)
    :param query: the user's query / question
    :param docsearch: FAISS wrapper from raw documents to search from based on the similarity search algos
    :param chain: the LLM chain object
    :return: the response from the LLM chain object
    """
    docs = docsearch.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return response


def faiss_vector_search(query: str) -> str:
    """
    this function is used to load the chain and sets it up for the agent to use
    :param query: the user's query / question
    :return: the response from the LLM chain object
    """
    chain = load_chain()
    docsearch = load_prerequisites_for_vector_search(reader)
    response = query_based_similarity_search(query, docsearch, chain)
    return response


def serp_api_search(query: str) -> str:
    """
    this function is used to search through the internet (SerpAPI)
    for nutrition/exercise information in case it doesn't require further clarification,
    but a simple univocal answer.
    :param query: the user's query / question
    :return: the response from the SerpAPI's query to Google
    """
    search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
    response = search.run(query)
    return response


# testing the functions and putting them up together
def main():
    query = "What is the best time to eat before exercise?"
    faiss_search = faiss_vector_search(query)
    google_search = serp_api_search(query)


if __name__ == "__main__":
    main()
