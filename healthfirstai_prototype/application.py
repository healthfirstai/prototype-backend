# Built in Module
import timeit
import asyncio
from numpy.typing import NDArray

# Langchain Imports
from langchain import SQLDatabase, SQLDatabaseChain, PromptTemplate, OpenAI, LLMChain
from langchain.chains import SQLDatabaseSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import get_openai_callback

# Local Imports
from knn3_nl_to_sql.database import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from knn3_nl_to_sql.redis_db import (
    get_tables,
    create_embeddings,
    create_embeddings_async,
    fill_template,
    fill_template_async,
)
from knn3_nl_to_sql.utils import (
    log_chain_info,
    parse_output,
    build_output,
    choose_model,
)

# Import Global Variables
from knn3_nl_to_sql.templates import (
    CHAIN_PROMPT_PREFIX,
    CHAIN_PROMPT_SUFFIX,
    DECIDER_PROMPT,
    SQL_PREFIX,
    SQL_CHAIN_PREFIX,
    SQL_SUFFIX,
    SQL_CHAIN_INTERACTIVE_PREFIX,
    CHAIN_INTERACTIVE_PROMPT_SUFFIX,
    EXAMPLES_TEMPLATE,
    FORMAT_INSTRUCTIONS,
    TABLE_INFO,
)


def setup_sequential_chain_db(
    verbose: bool,
    top_k: int,
    example: str,
) -> SQLDatabaseSequentialChain:
    """
    Setup the sequential chain
    Returns the chain to be executed
    """
    prompt = PromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        template=CHAIN_PROMPT_PREFIX + example + CHAIN_PROMPT_SUFFIX,
    )
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return SQLDatabaseSequentialChain.from_llm(
        llm=choose_model("text-davinci-003"),
        database=db,
        verbose=verbose,
        query_prompt=prompt,
        decider_prompt=DECIDER_PROMPT,
        return_direct=True,
        return_intermediate_steps=True,
        top_k=top_k,
    )


def setup_sql_chain(example: str, model_name: str) -> LLMChain:
    return LLMChain(
        llm=choose_model(model_name),
        prompt=PromptTemplate(
            input_variables=["input", "table_info"],
            template=SQL_CHAIN_PREFIX + example + CHAIN_PROMPT_SUFFIX,
        ),
    )


def setup_sql_chain_interactive(model_name: str) -> LLMChain:
    return LLMChain(
        llm=choose_model(model_name),
        prompt=PromptTemplate(
            input_variables=["input", "sql_input", "table_info"],
            template=SQL_CHAIN_INTERACTIVE_PREFIX + CHAIN_INTERACTIVE_PROMPT_SUFFIX,
        ),
    )


def setup_std_chain_db(
    verbose: bool,
    top_k: int,
    example: str,
    include_tables: list,
    sample_rows_in_table_info: int,
) -> SQLDatabaseChain:
    prompt = PromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        template=CHAIN_PROMPT_PREFIX + example + CHAIN_PROMPT_SUFFIX,
    )
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        # include_tables=include_tables,
        sample_rows_in_table_info=sample_rows_in_table_info,
    )
    print(db.table_info)
    return SQLDatabaseChain.from_llm(
        llm=OpenAI(model="text-davinci-003", temperature=0),
        db=db,
        verbose=verbose,
        prompt=prompt,
        use_query_checker=False,
        return_direct=True,
        return_intermediate_steps=True,
        top_k=top_k,
    )


def setup_agent_db(verbose: bool, top_k: int):
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(model="gpt-3.5-turbo"))
    return create_sql_agent(
        llm=choose_model("text-davinci-003"),
        toolkit=toolkit,
        verbose=verbose,
        prefix=SQL_PREFIX,
        suffix=SQL_SUFFIX,
        format_instructions=FORMAT_INSTRUCTIONS,
        top_k=top_k,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


def decide_include_tables(
    query_embedding: NDArray,
    tag: str = "get_tables",
    num_of_tables: int = 5,
) -> list[str]:
    return get_tables(query_embedding, tag, num_of_tables)


async def decide_include_tables_async(
    query_embedding: NDArray,
    tag: str = "get_tables",
    num_of_tables: int = 5,
):
    """
    Takes in a query embedding and returns a list of tables to include
    """
    return await asyncio.to_thread(
        decide_include_tables, query_embedding, tag, num_of_tables
    )


def execute_chain(
    user_input: str,
    db_chain,
    example_string: str,
    included_tables: list | None = None,
) -> dict:
    """
    Execute the chain & return the output dictionary
    """
    if included_tables is None:
        included_tables = []
    with get_openai_callback() as cb:
        start_time = timeit.default_timer()  # Start measuring execution time
        output = db_chain(user_input)
        end_time = timeit.default_timer()  # Stop measuring execution time
        output["total_tokens"] = cb.total_tokens
        output["prompt_tokens"] = cb.prompt_tokens
        output["completion_tokens"] = cb.completion_tokens
        output["total_cost"] = cb.total_cost
        output["example"] = example_string
        output["included_tables"] = included_tables or ""
        output["execution_time"] = end_time - start_time
        output["output_sql_query"] = output["intermediate_steps"][-2]["sql_cmd"]
    return output


def execute_agent(user_input: str, setup_func):
    with get_openai_callback() as cb:
        start_time = timeit.default_timer()  # Start measuring execution time
        output = setup_func(user_input)
        end_time = timeit.default_timer()
        output["total_tokens"] = cb.total_tokens
        output["prompt_tokens"] = cb.prompt_tokens
        output["completion_tokens"] = cb.completion_tokens
        output["total_cost"] = cb.total_cost
        output["execution_time"] = end_time - start_time
        output["output_sql_query"] = output["intermediate_steps"][-1][-2].tool_input
        output["result"] = output["intermediate_steps"][-1][-1]
    return output


def start_seq_chain(
    user_input: str,
    verbose: bool = False,
    top_k: int = 3,
) -> dict:
    """
    This function is used to start the sequential chain.
    Returns the output of the chain.
    """
    query_embedding = create_embeddings(user_input)
    example = fill_template(query_embedding, EXAMPLES_TEMPLATE)
    if verbose:
        log_chain_info(examples=example)
    db_chain = setup_sequential_chain_db(verbose, top_k, example)
    return execute_chain(user_input, db_chain, example)


async def start_seq_chain_async(
    user_input: str,
    verbose: bool = False,
    top_k: int = 3,
) -> dict:
    """
    This function is used to start the sequential chain.
    Returns the output of the chain.
    """
    query_embedding = await create_embeddings_async(user_input)
    example = await fill_template_async(query_embedding, EXAMPLES_TEMPLATE)
    if verbose:
        log_chain_info(examples=example)
    db_chain = setup_sequential_chain_db(verbose, top_k, example)
    return execute_chain(user_input, db_chain, example)


def start_std_chain(
    user_input: str,
    verbose: bool = False,
    top_k: int = 3,
) -> dict:
    """
    This function is used to start the standard chain.
    Returns the output of the chain.
    """
    query_embedding = create_embeddings(user_input)
    included_tables = decide_include_tables(query_embedding, num_of_tables=3)
    example = fill_template(query_embedding, EXAMPLES_TEMPLATE)
    if verbose:
        log_chain_info(tables=included_tables, examples=example)
    db_chain = setup_std_chain_db(
        verbose=verbose,
        top_k=top_k,
        include_tables=included_tables,
        example=example,
        sample_rows_in_table_info=3,
    )
    return execute_chain(user_input, db_chain, example, included_tables)


async def start_std_chain_async(
    user_input: str,
    verbose: bool = False,
    top_k: int = 3,
) -> dict:
    """
    This function is used to start the standard chain.
    Returns the output of the chain.
    """
    query_embedding = await create_embeddings_async(user_input)
    included_tables = await decide_include_tables_async(
        query_embedding, num_of_tables=3
    )
    example = await fill_template_async(query_embedding, EXAMPLES_TEMPLATE)
    if verbose:
        log_chain_info(tables=included_tables, examples=example)
    db_chain = setup_std_chain_db(
        verbose=verbose,
        top_k=top_k,
        include_tables=included_tables,
        example=example,
        sample_rows_in_table_info=1,
    )
    return execute_chain(user_input, db_chain, example, included_tables)


def get_table_info(included_tables: list, table_info: dict = TABLE_INFO) -> str:
    # sourcery skip: inline-immediately-returned-variable, use-join
    """
    Takes a list of tables and returns a string with the table information.
    """
    select_table_info = ""
    for table in included_tables:
        select_table_info += table_info[table] + "\n"
    return select_table_info


def start_sql_chain(
    user_input: str,
    verbose: bool = False,
    top_k: int = 3,
):
    """
    This function is used to start the standard chain.
    Returns the output of the chain.
    """
    query_embedding = create_embeddings(user_input)
    included_tables = decide_include_tables(query_embedding, num_of_tables=3)
    example = fill_template(query_embedding, EXAMPLES_TEMPLATE)
    select_table_info = get_table_info(included_tables)
    if verbose:
        log_chain_info(tables=included_tables, examples=example)
    db_chain = setup_sql_chain(
        example=example,
    )
    output = db_chain.generate(
        [
            {
                "input": user_input,
                "top_k": top_k,
                "table_info": select_table_info,
            }
        ]
    )
    return parse_output(output.generations[0][0].text)


async def start_sql_chain_interactive_async(
    sql_input: str,
    user_input: str,
    included_tables: list[str] | None,
    verbose: bool,
    model_name: str,
):
    """
    This function is used to start the interactive sql chain
    Returns the output of the chain.
    """
    try:
        query_embedding = await create_embeddings_async(user_input)
        included_tables = included_tables or await decide_include_tables_async(
            query_embedding, num_of_tables=3
        )
        select_table_info = get_table_info(included_tables)
        if verbose:
            log_chain_info(tables=included_tables)
        db_chain = setup_sql_chain_interactive(model_name)
        output = db_chain.generate(
            [
                {
                    "input": user_input,
                    "sql_input": sql_input,
                    "table_info": select_table_info,
                }
            ]
        )
        parsed_output = parse_output(output.generations[0][0].text)
        run_id = run_id[0].run_id if (run_id := output.run) else None
        llm_info = output.llm_output
        return build_output(parsed_output, included_tables, llm_info, run_id, verbose)
    except Exception as e:
        return build_output(error=e, included_tables=included_tables)


async def start_sql_chain_async(
    user_input: str,
    verbose: bool,
    model_name: str,
):
    """
    This function is used to start the sql chain.
    Returns the output of the chain.
    """
    try:
        query_embedding = await create_embeddings_async(user_input)
        included_tables = await decide_include_tables_async(
            query_embedding, num_of_tables=3
        )
        example = await fill_template_async(query_embedding, EXAMPLES_TEMPLATE)
        select_table_info = get_table_info(included_tables)
        if verbose:
            log_chain_info(tables=included_tables, examples=example)
        db_chain = setup_sql_chain(example=example, model_name=model_name)
        output = db_chain.generate(
            [
                {
                    "input": user_input,
                    "table_info": select_table_info,
                }
            ]
        )
        parsed_output = parse_output(output.generations[0][0].text)
        run_id = run_id[0].run_id if (run_id := output.run) else None
        llm_info = output.llm_output
        return build_output(parsed_output, included_tables, llm_info, run_id, verbose)
    except Exception as e:
        return build_output(error=e)


def start_sql_agent(
    user_input: str,
    verbose: bool = False,
    top_k: int = 3,
):
    return execute_agent(user_input, setup_agent_db(verbose, top_k))
