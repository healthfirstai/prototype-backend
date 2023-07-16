# NOTE: This is an example of how to interact with Redis from Python
# The code does not work as is, but is helpful as a reference.
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

from healthfirstai_prototype.database import REDIS_HOST, REDIS_PORT, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))


NUTRITION_INDEX_NAME = "nut_index"  # Vector Index Name
NUTRITION_DOC_PREFIX = "nut_doc:"  # RediSearch Key Prefix for the Index

EXAMPLE_INDEX_NAME = "example_index"  # Vector Index Name
EXAMPLE_DOC_PREFIX = "example_doc:"  # RediSearch Key Prefix for the Index


def get_redis_connection():
    return redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))


def create_nutrition_index(
    vector_dimensions: int = 112,
    index_name: str = NUTRITION_INDEX_NAME,
    doc_prefix: str = NUTRITION_DOC_PREFIX,
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


def search_similar_food(
    food_id: int,
    tag: str,
    num_of_results: int,
) -> list[str]:
    """
    Get the top n most nutritionally similar foods to the given food
    """
    query = (
        Query("(@tag:{ get_similar_foods })=>[KNN 1 @vector $vec as score]")
        .sort_by("score")
        .return_fields("food_name")
        .paging(0, num_of_results)
        .dialect(2)
    )

    # query_embedding is a numpy array
    query_params = {"vec": find_vec(food_id).tobytes()}
    table_doc_list = r.ft(NUTRITION_INDEX_NAME).search(query, query_params).docs
    print(table_doc_list)
    return [doc.table_name for doc in table_doc_list]


def insert_foods(
    food: List[tuple],
) -> List:
    """
    Store food vectors in Redis
    """
    # Write to Redis
    pipe = r.pipeline()
    for id, food_name, food_group, vector in food:
        pipe.hset(
            f"{NUTRITION_DOC_PREFIX}{id}",
            mapping={
                "vector": np.array(vector).tobytes(),
                "food_name": food_name,
                "food_group": food_group,
                "tag": "get_similar_foods",
            },
        )
    return pipe.execute()


def find_vec(
    food_id: int,
):
    """
    Store food vectors in Redis
    """
    val = r.hget(f"{NUTRITION_DOC_PREFIX}{food_id}", "vector")
    return np.frombuffer(val, dtype=np.float32)


def main():
    pass


if __name__ == "__main__":
    main()
