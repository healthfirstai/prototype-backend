from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY") or ""

# Create the PromptTemplate
template = "Question: {question}\nAnswer: Let's think step by step."

# Create the LLMChain
llm_chain = LLMChain(
    llm=Cohere(
        client=None,
        cohere_api_key=COHERE_API_KEY,
    ),
    prompt=PromptTemplate(input_variables=["question"], template=template),
)

# Run the LLMChain
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
response = llm_chain.run(question)
