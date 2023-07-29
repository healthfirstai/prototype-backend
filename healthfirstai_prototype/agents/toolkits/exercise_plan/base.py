import openai
from langchain import SQLDatabaseChain, SQLDatabase
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.enums.openai_enums import ModelName
from .utils import generate_schedule_json
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER") or ""
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or ""
DB_HOST = os.getenv("POSTGRES_HOST") or ""
DB_NAME = os.getenv("POSTGRES_DATABASE") or ""
DB_PORT = os.getenv("POSTGRES_PORT") or ""
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = f"{OPENAI_API_KEY}"


def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == "exit":
            print("Exiting...")
            break
        else:
            try:
                question = QUERY.format(question=prompt, user_id=1)
                print(db_chain.run(question))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    generate_schedule_json(1)
    llm = get_model(ModelName.gpt_3_5_turbo)
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())

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
