# NOTE: Any functions that are used in multiple files should be placed here
from openai.error import RateLimitError
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, Cohere
from uuid import UUID
import sys
import timeit
from typing import List
from healthfirstai_prototype.util_models import ModelName

from langchain.prompts.prompt import PromptTemplate


def get_model(model_name: str) -> ChatOpenAI | OpenAI:
    """
    Choose the model to use
    Returns the model class
    """
    if model_name == ModelName.gpt_3_5_turbo:
        return ChatOpenAI(client=None, model=ModelName.gpt_3_5_turbo, temperature=0)
    elif model_name == ModelName.text_davinci_003:
        return OpenAI(client=None, model=ModelName.text_davinci_003, temperature=0)
    else:
        raise ValueError("Model name not recognized")
