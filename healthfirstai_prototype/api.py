from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from healthfirstai_prototype.application import (
    start_std_chain_async,
    start_sql_chain_interactive_async,
    start_sql_agent,
    start_seq_chain_async,
    start_sql_chain_async,
)

app = FastAPI()


class ExecName(str, Enum):
    sql_chain = "sql_chain"
    standard_chain = "std_chain"
    sequential_chain = "seq_chain"
    sql_agent = "sql_agent"


class ModelName(str, Enum):
    gpt_3_5_turbo = "gpt-3.5-turbo"
    davinci003 = "text-davinci-003"


class UserInput(BaseModel):
    user_input: str = ""
    exec_type: ExecName = ExecName.sql_chain
    verbose: bool = False


class UserInputInteractive(BaseModel):
    user_input: str = ""
    sql_input: str = ""
    included_tables: list[str] | None = []
    model_name: ModelName = ModelName.davinci003
    verbose: bool = True


@app.get("/")
async def root():
    return {"status": "Web server working"}


@app.post("/chat_to_sql_interactive/")
async def chat_to_sql_interactive(user_input: UserInputInteractive):
    """
    This is the main endpoint for interactive chat to SQL conversion.

    Args:
        - user_input (UserInputInteractive): An object representing the user input.
            - user_input.user_input (str): The user's input for the chat.
            - user_input.sql_input (str, optional): The initial SQL query (if provided).
            - user_input.included_tables (List[str], optional): List of included tables in the SQL query.
            - user_input.verbose (bool, optional): Flag indicating verbose output.
            - user_input.model_name (str, optional): The name of the model used for conversion.

    Returns:
        dict: A JSON object with the following keys:
            - "sql" (str): The revised SQL query.
            - "ok" (bool): Whether the query was successful.
            - "error" (str): The error message if the query was unsuccessful.
            - "record_id" (str): The record ID of the query.

    Raises:
        HTTPException: If user input is missing or included tables are missing when SQL query is provided.
    """
    if not user_input.user_input:
        raise HTTPException(status_code=404, detail="User input not provided")
    if user_input.sql_input and not user_input.included_tables:
        raise HTTPException(status_code=404, detail="Included tables not found")

    if user_input.sql_input:
        return await start_sql_chain_interactive_async(
            user_input.sql_input,
            user_input.user_input,
            user_input.included_tables,
            user_input.verbose,
            user_input.model_name,
        )
    else:
        return await start_sql_chain_async(
            user_input.user_input,
            user_input.verbose,
            user_input.model_name,
        )


@app.post("/chat_to_sql/")
async def chat_to_sql(user_input: UserInput):
    """
    This is the main endpoint for the chatbot. It takes in a user input
    Returns a JSON object with the following keys:
    - "sql": The SQL query
    - "ok": Whether the query was successful
    - "error": The error message if the query was unsuccessful
    - "record_id": The record ID of the query
    """
    return await start_sql_chain_async(
        user_input.user_input,
        user_input.verbose,
        "text-davinci-003",
    )


@app.post("/chat_to_sql_test/")
async def chat_to_sql_test(user_input: UserInput):
    """
    This is an endpoint to test the chatbot. It takes in a user input, and the name of the execution method.
    """
    if user_input.exec_type is ExecName.standard_chain:
        return await start_std_chain_async(user_input.user_input, user_input.verbose, 3)

    elif user_input.exec_type is ExecName.sequential_chain:
        return await start_seq_chain_async(user_input.user_input, user_input.verbose, 3)

    elif user_input.exec_type is ExecName.sql_agent:
        return start_sql_agent(user_input.user_input, user_input.verbose, 3)

    raise HTTPException(status_code=404, detail="ExecName not found")
