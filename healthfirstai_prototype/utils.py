# NOTE: Any functions that are used in multiple files should be placed here
from openai.error import RateLimitError
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, Cohere
from uuid import UUID
import sys
import timeit
from typing import List

from langchain.prompts.prompt import PromptTemplate


# TODO: Change this to accept keyword args
def log_chain_info(
    tables: List[str] | None = None,
    examples: str = "",
) -> None:
    """
    Log examples and tables to a file
    """
    if tables is None:
        tables = []
    sys.stdout.write("Logging examples and tables to file\n")
    sys.stdout.write(str(tables) + "\n")
    sys.stdout.write(examples)


def execute_and_time(func, **kwargs):
    """
    Execute and time the execution of a function
    """
    start_time = timeit.default_timer()  # Start measuring execution time
    output = func(**kwargs)
    end_time = timeit.default_timer()  # Stop measuring execution time
    output["execution_time"] = end_time - start_time
    return output


def construct_chain_prompt(
    prefix: str,
    example: str,
    suffix: str,
) -> PromptTemplate:
    """
    Construct a prompt for the chain with example and table info
    Returns a PromptTemplate object
    """
    return PromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        template=prefix + example + suffix,
    )


# TODO: I don't really know the best practice of how to parse the output
def parse_output(output: str) -> str:
    """
    Parse the output from the model
    """
    return output.split(":")[1].strip()


def choose_model(model_name: str) -> ChatOpenAI | OpenAI:
    """
    Choose the model to use
    Returns the model class
    """
    if model_name == "gpt-3.5-turbo":
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    elif model_name == "text-davinci-003":
        return OpenAI(model="text-davinci-003", temperature=0)
    else:
        raise ValueError("Model name not recognized")


def build_output(
    sql_output: str = "",
    included_tables: list[str] | None = None,
    llm_info: dict | None = None,
    run_id: UUID | None = None,
    verbose: bool = False,
    error=None,
) -> dict:
    """
    Build the json object from the model output
    """
    # TODO: Auto increment record_id
    data = {}
    data["record_id"] = run_id
    if verbose:
        data["included_tables"] = included_tables
        data["llm_info"] = llm_info

    if error == RateLimitError:  # Rate limit exception
        data["ok"] = 3
        data["error"] = str(error)
    elif error:  # General Failure
        data["ok"] = 0
        data["error"] = str(error)
    elif sql_output:  # Success
        data["ok"] = 1
        data["sql"] = sql_output
    else:
        data["ok"] = 2
        data["error"] = "Query not within the scope of our database"
    return data
