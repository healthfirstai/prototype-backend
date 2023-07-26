from PyPDF2 import PdfReader
from healthfirstai_prototype.data_models import User
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# NOTE: Use this class in the future to implement the evaluation techniques
from langchain.evaluation import QAEvalChain
import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""
SERPER_API_KEY = os.getenv("SERPER_API_KEY") or ""


def read_pdf(
    path_to_pdf: str = "../notebooks/pdfs/Sports-And-Exercise-Nutrition.pdf",
) -> PdfReader:
    """
    This function is simply taking the path to the PDF file and returning the PDFReader object

    Params:
        path_to_pdf (str, optional) : The path to the PDF file

    Returns:
        The PDF file in the PDFReader format
    """
    return PdfReader(path_to_pdf)


# NOTE: this function is not used yet
def parse_user_info(user_data: User) -> dict[str, str]:
    """
    This function is used to parse the user's personal information

    Params:
        user_data (int) : User's personal information

    Returns:
        a dictionary containing the user's personal information
    """
    return {
        "height": str(user_data.height),
        "weight": str(user_data.weight),
        "gender": str(user_data.gender),
        "age": str(user_data.age),
        "city_id": str(user_data.city_id),
        "country_id": str(user_data.country_id),
    }


def collect_raw_text_from_pdf_data(reader: PdfReader) -> str:
    """
    This function is used to collect raw text from the PDF file

    Params:
        reader (PdfReader) : The PDF file in the PDFReader format

    Returns:
        raw text collected from PDF file
    """
    raw_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text


def split_text(raw_text: str) -> list[str]:
    """
    This function is used to split the raw text into chunks

    Params:
        raw_text (str) : raw text collected from the PDF file

    Returns:
        a list of text chunks
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    return text_splitter.split_text(raw_text)


# NOTE: think of how this fucntion's output could be stored in Weaviate
def embed_text(texts: list[str]) -> FAISS:
    """
    This function is embedding the text using the Cohere embedding + FAISS library

    Params:
        texts (list[str]) : a list of text chunks

    Returns:
        FAISS wrapper from raw documents
    """
    # Download embeddings from Cohere
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)  # type: ignore
    # Construct FAISS wrapper from raw documents
    docsearch = FAISS.from_texts(texts, embeddings)  # type: ignore

    return docsearch


def load_prerequisites_for_vector_search(reader: PdfReader) -> FAISS:
    """
    This function is used to load the prerequisites for the agent to use

    Params:
        reader (PdfReader) : The PDF file in the PDFReader format

    Returns:
        FAISS wrapper from raw documents
    """
    raw_text = collect_raw_text_from_pdf_data(reader)
    texts = split_text(raw_text)
    docsearch = embed_text(texts)
    return docsearch


# def scoring_with_faiss(query, faiss_search_result, google_search_result):
#     evaluator = load_evaluator("pairwise_string", requires_reference=True)

#     evaluator.evaluate_string_pairs(
#         prediction="there are three dogs",
#         prediction_b="4",
#         input="how many dogs are in the park?",
#         reference="four",
#     )
