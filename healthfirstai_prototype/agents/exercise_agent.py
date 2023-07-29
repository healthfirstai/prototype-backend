from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from healthfirstai_prototype.models.database import OPENAI_API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

db = SQLDatabase.from_uri(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-0613")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run("What is the best chest exercise?")
