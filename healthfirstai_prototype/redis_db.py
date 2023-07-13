import redis
from redis.cluster import RedisCluster, ClusterNode
import asyncio
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from typing import List

from numpy.typing import NDArray
import openai
import numpy as np

import json

from knn3_nl_to_sql.database import REDIS_HOST, REDIS_PORT, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))


TABLE_INDEX_NAME = "table_index"  # Vector Index Name
TABLE_DOC_PREFIX = "table_doc:"  # RediSearch Key Prefix for the Index

EXAMPLE_INDEX_NAME = "example_index"  # Vector Index Name
EXAMPLE_DOC_PREFIX = "example_doc:"  # RediSearch Key Prefix for the Index


def get_redis_connection():
    return redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))


def create_example_index(
    vector_dimensions: int = 1536,
    index_name: str = "example_index",
    doc_prefix: str = EXAMPLE_DOC_PREFIX,
):
    """
    Create a new index with the given vector dimensions
    """
    try:
        r.ft(index_name).info()
        print("Index already exists!")
    except Exception:
        schema = (
            TagField("tag"),  # Tag Field Name
            VectorField(
                "vector",  # Vector Field Name
                "FLAT",
                {  # Vector Index Type: FLAT or HNSW
                    "TYPE": "FLOAT32",  # FLOAT32 or FLOAT64
                    "DIM": vector_dimensions,  # Number of Vector Dimensions
                    "DISTANCE_METRIC": "COSINE",  # Vector Search Distance Metric
                },
            ),
        )

        # index Definition
        definition = IndexDefinition(prefix=[doc_prefix], index_type=IndexType.HASH)

        # create Index
        r.ft(index_name).create_index(fields=schema, definition=definition)


def create_table_index(
    vector_dimensions: int = 1536,
    index_name: str = "table_index",
    doc_prefix: str = TABLE_DOC_PREFIX,
):
    """
    Create a new index with the given vector dimensions
    """
    try:
        r.ft(index_name).info()
        print("Index already exists!")
    except Exception:
        schema = (
            TagField("tag"),  # Tag Field Name
            VectorField(
                "vector",  # Vector Field Name
                "FLAT",
                {  # Vector Index Type: FLAT or HNSW
                    "TYPE": "FLOAT32",  # FLOAT32 or FLOAT64
                    "DIM": vector_dimensions,  # Number of Vector Dimensions
                    "DISTANCE_METRIC": "COSINE",  # Vector Search Distance Metric
                },
            ),
        )

        # index Definition
        definition = IndexDefinition(prefix=[doc_prefix], index_type=IndexType.HASH)

        # create Index
        r.ft(index_name).create_index(fields=schema, definition=definition)


def flush_all():
    """
    Flush all documents from the index
    """
    r.execute_command("FLUSHALL")


# TODO: Move this to utils.py
def load_tables(
    tables_filename: str = "tables.json",
    tables_dirname: str = "init_redis",
) -> List[dict]:
    """
    Load tables.json file
    """
    with open(f"knn3_nl_to_sql/{tables_dirname}/{tables_filename}", "r") as f:
        tables = json.load(f)
    return tables


def create_embeddings(to_vec_input: List[str] | str) -> NDArray:
    """
    Create embeddings for a list of strings
    Returns a numpy array of embeddings
    """
    new_input = to_vec_input
    if type(to_vec_input) is str:
        new_input = [to_vec_input]
    response = openai.Embedding.create(
        input=new_input,
        engine="text-embedding-ada-002",
    )
    return np.array([r["embedding"] for r in response["data"]], dtype=np.float32)


async def create_embeddings_async(to_vec_input: List[str] | str) -> NDArray:
    """
    Create embeddings for a list of strings
    Returns a numpy array of embeddings
    """
    return await asyncio.to_thread(create_embeddings, to_vec_input)


def get_tables(
    query_embedding: NDArray,
    tag: str,
    num_of_tables: int,
) -> list[str]:
    """
    Get the top n most semantically similar tables to the user query
    """
    query = (
        Query(
            "(@tag:{ "
            + tag
            + " })=>[KNN "
            + str(num_of_tables)
            + " @vector $vec as score]"
        )
        .sort_by("score")
        .return_fields("table_name", "tag", "score")
        .paging(0, num_of_tables)
        .dialect(2)
    )

    query_params = {"vec": query_embedding.tobytes()}
    table_doc_list = r.ft(TABLE_INDEX_NAME).search(query, query_params).docs
    return [doc.table_name for doc in table_doc_list]


def get_examples(
    query_embedding: NDArray,
    tag: str = "get_example_queries",
    num_of_examples: int = 1,
) -> tuple[str, str]:
    """
    Get the most relavent example query to the user query
    """
    query = (
        Query(
            "(@tag:{ "
            + tag
            + " })=>[KNN "
            + str(num_of_examples)
            + " @vector $vec as score]"
        )
        .sort_by("score")
        .return_fields("user_input", "correct_sql_query", "tag", "score")
        .paging(0, num_of_examples)
        .dialect(2)
    )

    query_params = {"vec": query_embedding.tobytes()}
    example_doc_list = r.ft(EXAMPLE_INDEX_NAME).search(query, query_params).docs
    return example_doc_list[0].user_input, example_doc_list[0].correct_sql_query


async def get_examples_async(
    query_embedding: NDArray,
    tag: str = "get_example_queries",
    num_of_examples: int = 1,
) -> tuple[str, str]:
    """
    Get the most relavent example query to the user query
    """
    return await asyncio.to_thread(get_examples, query_embedding, tag, num_of_examples)


def fill_template(query_embedding: NDArray, example_template: str) -> str:
    """
    Fill in the template with the user query and corresponding the example query
    """
    user_input, sql_query = get_examples(query_embedding)
    return example_template.format(user_input=user_input, sql_query=sql_query)


async def fill_template_async(query_embedding: NDArray, example_template: str) -> str:
    """
    Fill in the template with the user query and corresponding the example query
    """
    return await asyncio.to_thread(fill_template, query_embedding, example_template)


def insert_tables(
    tables: List[dict],
) -> List:
    """
    Embed table_schema, table_description
    Store table_name
    Returns result from Redis
    """

    table_name_list = [table["table_name"] for table in tables]
    table_schema_list = [table["table_schema"] for table in tables]
    table_description_list = [table["table_description"] for table in tables]

    schema_vecs = create_embeddings(table_schema_list)
    description_vecs = create_embeddings(table_description_list)

    # Write to Redis
    pipe = r.pipeline()
    for i, (s_embedding, d_embedding) in enumerate(zip(schema_vecs, description_vecs)):
        pipe.hset(
            f"{TABLE_DOC_PREFIX}{i}",
            mapping={
                "vector": d_embedding.tobytes(),
                "schema_vec": s_embedding.tobytes(),
                "table_name": table_name_list[i],
                "tag": "get_tables",
            },
        )
    return pipe.execute()


def insert_examples(
    tables: List[dict],
) -> List:
    """
    Embed user_input
    Store executable, difficulty_level, correct_sql_query
    """

    user_input_list = []
    executable_list = []
    difficulty_level_list = []
    correct_sql_query_list = []

    for table in tables:
        user_input = table.get("user_input", "")
        executable = str(table.get("executable", False))
        difficulty_level = table.get("difficulty_level", "")
        correct_sql_query = table.get("correct_sql_query", "")

        user_input_list.append(user_input)
        executable_list.append(executable)
        difficulty_level_list.append(difficulty_level)
        correct_sql_query_list.append(correct_sql_query)

    user_input_vecs = create_embeddings(user_input_list)

    # Write to Redis
    pipe = r.pipeline()
    for i, user_input_embedding in enumerate(user_input_vecs):
        pipe.hset(
            f"{EXAMPLE_DOC_PREFIX}{i}",
            mapping={
                "vector": user_input_embedding.tobytes(),
                "user_input": user_input_list[i],
                "executable": executable_list[i],
                "difficulty_level": difficulty_level_list[i],
                "correct_sql_query": correct_sql_query_list[i],
                "tag": "get_example_queries",
            },
        )
    return pipe.execute()


def main():
    pass


if __name__ == "__main__":
    main()
