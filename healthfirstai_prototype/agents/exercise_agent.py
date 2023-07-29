from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from healthfirstai_prototype.enums.openai_enums import ModelName
from healthfirstai_prototype.models.database import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)
from healthfirstai_prototype.utils import get_model

db = SQLDatabase.from_uri(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
llm = get_model(ModelName.gpt_3_5_turbo_0613)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run("What is the best chest exercise?")
