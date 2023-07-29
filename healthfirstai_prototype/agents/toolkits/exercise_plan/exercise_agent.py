# NOTE: This is where the main application logic is implemented for the exercise agent
import json

import openai
from langchain import SQLDatabaseChain, SQLDatabase
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    conversation = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory()
    )

    # Create query instruction
    QUERY = """
    Given an input question and the user_id is {user_id}, first create a syntactically correct postgresql query to run, 
    then look at the results of the query and return the answer. Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    {question}
    """

    # Set up the database chain
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

    # get_prompt()
