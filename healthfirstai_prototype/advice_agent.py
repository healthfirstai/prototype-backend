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

"""
Facebook AI Similarity Search (Faiss) is a library for efficient similarity search and clustering of dense vectors. It contains algorithms 
that search in sets of vectors of any size, up to ones that possibly do not fit in RAM. It also contains supporting code for evaluation 
and parameter tuning.
"""

# Load env file
load_dotenv()

# Load API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""

# location of the pdf file/files.
path_to_pdf = "../notebooks/pdfs/Sports-And-Exercise-Nutrition.pdf"
reader = PdfReader(path_to_pdf)

# read data from the file and put them into a variable called raw_text
# FIXME: refactor the code here


def collect_raw_text_from_pdf_data(reader: PdfReader) -> str:
    raw_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    print("Raw text collected from PDF file...")
    return raw_text


def clean_raw_text(raw_text: str) -> str:
    # FIXME: preprocess the raw text and work more with irregularities in the text
    # REFER to this conversation: https://chat.openai.com/share/34e754f5-7342-4b17-a6ff-dc8b3487fd6a

    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r"\s+", " ", raw_text)

    # Remove unwanted characters, such as special characters and non-breaking spaces
    cleaned_text = re.sub(r"[^\x00-\x7F]", "", cleaned_text)

    # Remove any remaining leading/trailing spaces and newline characters
    cleaned_text = cleaned_text.strip()
    print("Raw text cleaned...")
    return cleaned_text


def split_text(raw_text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1024,
        chunk_overlap=256,
        length_function=len,
    )

    return text_splitter.split_text(raw_text)


def embed_text(texts: str) -> FAISS:
    # Download embeddings from Cohere
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)  # type: ignore
    # Construct FAISS wrapper from raw documents
    docsearch = FAISS.from_texts(texts, embeddings)  # type: ignore

    return docsearch


def load_chain() -> BaseCombineDocumentsChain:
    chain = load_qa_chain(
        Cohere(cohere_api_key=COHERE_API_KEY, verbose=True),  # type: ignore
        # FIXME: think about the chain_type!!
        chain_type="stuff",
        verbose=True,
    )
    return chain


def query_based_similarity_search(
    query: str, docsearch: FAISS, chain: BaseCombineDocumentsChain
) -> str:
    docs = docsearch.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return response
