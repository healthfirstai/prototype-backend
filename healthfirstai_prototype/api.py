# NOTE: This is an example of a FastAPI server.
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()


# NOTE: Example of a Enum class
class ExecName(str, Enum):
    sql_chain = "sql_chain"
    standard_chain = "std_chain"
    sequential_chain = "seq_chain"
    sql_agent = "sql_agent"


# NOTE: Example of a Pydantic Data Model
class UserInput(BaseModel):
    user_input: str = ""
    exec_type: ExecName = ExecName.sql_chain
    verbose: bool = False


class UserInputInteractive(BaseModel):
    user_input: str = ""
    sql_input: str = ""
    included_tables: list[str] | None = []
    verbose: bool = True


@app.get("/")
async def root():
    return {"status": "Hello world!"}


# NOTE: Example of a POST endpoint and its corresponding documentation
@app.post("/chat_to_sql_interactive/")
async def chat_to_sql_interactive(user_input: UserInput):
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

    # NOTE: Return awaited value
