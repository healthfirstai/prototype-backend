import os
from dotenv import load_dotenv
from healthfirstai_prototype.advice_chains import (
    faiss_vector_search,
    serp_api_search,
)

from healthfirstai_prototype.advice_tools import read_pdf

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


# testing the functions and putting them up together
def main():
    query = "What is the best time to eat before exercise?"
    pdf_reader = read_pdf()
    google_search_results = serp_api_search(query)
    faiss_search_results = faiss_vector_search(query, pdf_reader)
    print("--------------------------------------")
    print("Query: ", query)
    print("--------------------------------------")
    print("KB response: ", faiss_search_results)
    print("--------------------------------------")
    print("Google Search: ", google_search_results)
    print("--------------------------------------")


if __name__ == "__main__":
    main()
