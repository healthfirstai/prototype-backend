"""Utility Functions

This file contains the utility functions used project-wide. Any function that is used repeatedly in multiple files should be defined here.

"""
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from healthfirstai_prototype.util_models import ModelName
from langchain.embeddings import OpenAIEmbeddings
import redis

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def get_model(model_name: str) -> ChatOpenAI | OpenAI:
    """
    Creates and returns an instance of the required model.

    The function takes as input the name of the model and returns the corresponding model instance.
    If the model name is not recognized, a ValueError is raised.

    Args:
        model_name: The name of the model.

    Returns:
        An instance of the corresponding model.

    Raises:
        ValueError: If the model name is not recognized.
    """
    if model_name == ModelName.gpt_3_5_turbo:
        return ChatOpenAI(
            client=None,
            model=ModelName.gpt_3_5_turbo,
            temperature=0,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
    elif model_name == ModelName.gpt_3_5_turbo_0613:
        return ChatOpenAI(
            client=None,
            model=ModelName.gpt_3_5_turbo_0613,
            temperature=0,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
    elif model_name == ModelName.text_davinci_003:
        return OpenAI(
            client=None,
            model=ModelName.text_davinci_003,
            temperature=0,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
    else:
        raise ValueError("Model name not recognized")


def get_embedding_model(model_name: str) -> OpenAIEmbeddings:
    """
    Creates and returns an instance of the required embedding model.

    The function takes as input the name of the embedding model and returns the corresponding model instance.
    If the model name is not recognized, a ValueError is raised.

    Args:
        model_name: The name of the embedding model.

    Returns:
        OpenAIEmbeddings: An instance of the corresponding embedding model.

    Raises:
        ValueError: If the model name is not recognized.
    """
    if model_name == ModelName.text_embedding_ada_002:
        return OpenAIEmbeddings(
            client=None,
            model=ModelName.text_embedding_ada_002,
            chunk_size=1000,
        )
    else:
        raise ValueError("Model name not recognized")


def connect_to_redis() -> redis.Redis:
    """
    Creates and returns an instance of the required redis client.

    Returns:
        An instance of the corresponding redis client.
    """
    return redis.Redis(host="localhost", port=6379, db=0)
