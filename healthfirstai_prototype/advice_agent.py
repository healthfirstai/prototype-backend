# NOTE: Yan is working on this

"""
this agent is created for a number of goals/functions. the primary goal for this file is to provide a way to process user queries which require
information about nutrition and exercise. so, this is more of a knowledge base/advice providing agent.

1. to provide a way to search through the nutrition knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)
2. to provide a gateway for the user to search through the internet (SerpAPI) for nutrition/exercise information 
3. get user's personal information

CREATE TABLE “user”
(
    “id”         SERIAL PRIMARY KEY,
    “height”     DECIMAL(5, 2) NOT NULL,
    “weight”     DECIMAL(5, 2) NOT NULL,
    “gender”     VARCHAR(10)   NOT NULL CHECK (“gender” IN ('Male', 'Female', 'Other')),
    “age”        INT           NOT NULL,
    “country_id” INT           NOT NULL,
    “city_id”    INT           NOT NULL,
    FOREIGN KEY (“country_id”) REFERENCES “country” (“id”) ON DELETE CASCADE,
    FOREIGN KEY (“city_id”) REFERENCES “city” (“id”) ON DELETE CASCADE
);

"""

import os
import re
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Cohere
from langchain.utilities import GoogleSerperAPIWrapper
import pprint
import requests
import json
from healthfirstai_prototype.generate import get_user_info

# from langchain.evaluation import load_evaluator

"""
Facebook AI Similarity Search (Faiss) is a library for efficient similarity search and clustering of dense vectors. It contains algorithms 
that search in sets of vectors of any size, up to ones that possibly do not fit in RAM. It also contains supporting code for evaluation 
and parameter tuning.
"""

# Load env file
load_dotenv()

# Load API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""
SERPER_API_KEY = os.getenv("SERPER_API_KEY") or ""

# location of the pdf file/files.
path_to_pdf = "../notebooks/pdfs/Sports-And-Exercise-Nutrition.pdf"
reader = PdfReader(path_to_pdf)


# FIXME: add datatypes
def parse_user_info(user_data):
    """
    this function is used to get the user's personal information
    """
    # I dont know how does the user's info look like. Need to reconfigure the docker-compose file, especially the mount volume part
    pass


def collect_raw_text_from_pdf_data(reader: PdfReader) -> str:
    raw_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    print("Raw text collected from PDF file...")
    return raw_text


def split_text(raw_text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    return text_splitter.split_text(raw_text)


def embed_text(texts: list[str]) -> FAISS:
    """
    this function is embedding the text using the Cohere embedding + FAISS library
    """
    # Download embeddings from Cohere
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)  # type: ignore
    # Construct FAISS wrapper from raw documents
    docsearch = FAISS.from_texts(texts, embeddings)  # type: ignore

    return docsearch


def load_chain() -> BaseCombineDocumentsChain:
    """
    this function is loading the chain and sets it up for the agent to use
    """
    chain = load_qa_chain(
        Cohere(cohere_api_key=COHERE_API_KEY, verbose=True),  # type: ignore
        chain_type="map_reduce",
        # Setting verbose to True will print out some internal states of the Chain object while it is being ran.
        verbose=True,
    )
    return chain


def query_based_similarity_search(
    query: str, docsearch: FAISS, chain: BaseCombineDocumentsChain
) -> str:
    """
    this function is used to search through the knowledge base (aka book stored in the PDF file under the notebooks/pdfs/ folder)
    """
    docs = docsearch.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return response


def load_prerequisites_for_vector_search(reader: PdfReader) -> FAISS:
    raw_text = collect_raw_text_from_pdf_data(reader)
    texts = split_text(raw_text)
    docsearch = embed_text(texts)
    return docsearch


def faiss_vector_search(query: str) -> str:
    """
    this function is used to load the chain and sets it up for the agent to use
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
    """
    search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
    response = search.run(query)
    return response


# testing the functions and putting them up together
def main():
    query = "What is the best time to eat before exercise?"
    faiss_search = faiss_vector_search(query)
    google_search = serp_api_search(query)
    print("KB response: ", faiss_search)
    print("Google Search: ", google_search)


if __name__ == "__main__":
    main()
