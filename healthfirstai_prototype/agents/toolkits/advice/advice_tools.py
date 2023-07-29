import os
import pinecone
from healthfirstai_prototype.models.data_models import User
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

# Load env file
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or ""
PINECONE_ENV_NAME = os.getenv("PINECONE_ENV_NAME") or ""


def read_pdfs(
    folder_path: str = "../notebooks/pdfs/",
):
    """
    This function is simply taking the path to the PDF file, loading all the PDFs
    inside the folder and returning them as a List of Documents.

    Params:
        folder_path (str, optional): The path to the folder with PDF files

    Returns:
        documents (List[Documents]): The list of documents
    """
    loader = PyPDFDirectoryLoader(path=folder_path)
    return loader.load()


def split_documents(documents) -> list[str]:
    """
    This function is used to split the raw text into chunks

    Params:
        raw_text (str) : raw text collected from the PDF file

    Returns:
        texts (List[str]): a list of text chunks
    """
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    texts = text_splitter.split_text(documents)

    return texts


def prereqs_for_embeds(texts):
    docs = []
    metadatas = []
    for text in texts:
        docs.append(text.page_content)
        metadatas.append(text.metadata)

    return {"documents": docs, "metadatas": metadatas}


def pinecone_init(
    indexname: str = "pinecone-knowledge-base", vector_dimension: int = 4096
):
    """
    This function is used to initialize the Pinecone index.

    Params:
        indexname (str, optional): The name of the index (or simople the name of the database we are creating)

    Returns:
        index (Index): client for interacting with a Pinecone index via REST API
    """
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV_NAME)

    if indexname not in pinecone.list_indexes():
        # we create a new index if not exists
        pinecone.create_index(
            name=indexname,
            metric="cosine",
            dimension=vector_dimension,
        )

    # connect to the new index
    index = pinecone.Index(indexname)
    return index


def pinecone_insert(
    index: pinecone.Index,
    docs,
    metadatas,
):
    """
    This function is used to insert the documents into the Pinecone index. Please give it some
    time to index the documents before querying it.

    Params:
        index (Pinecone) : Pinecone index object
        docs (list[str]) : a list of text chunks
        metadatas (list[dict['str': 'str']]) : a list of metadata for each text chunk

    Returns:
        None
    """
    embedding_function = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)  # type: ignore
    vectorstore = Pinecone(index, embedding_function.embed_query, "text")
    vectorstore.add_texts(docs, metadatas)

    return


def query_pinecone_index(query: str, indexname: str = "pinecone-knowledge-base"):
    """
    This function is used to query the Pinecone index

    Params:
        query (str) : The user's query / question
        indexname (str) : Name of the Pinecone index object

    Returns:
        response (list[Document]): The response object from the Pinecone index
    """
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV_NAME)
    embedding_function = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)  # type: ignore
    docsearch = Pinecone.from_existing_index(indexname, embedding_function)
    response = docsearch.similarity_search(query)
    return response


def pinecone_delete(indexname: str = "pinecone-knowledge-base"):
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV_NAME)

    if indexname in pinecone.list_indexes():
        pinecone.delete_index(indexname)

    return


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


def main():
    query = "How many hours a day should I have?"

    print("--------------------------------------")
    print("Query: ", query)
    print("--------------------------------------")
    print(query_pinecone_index(query))


if __name__ == "__main__":
    main()
