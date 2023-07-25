from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from healthfirstai_prototype.util_models import ModelName
from langchain.embeddings import OpenAIEmbeddings

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def get_model(model_name: str) -> ChatOpenAI | OpenAI:
    """
    Choose the model to use
    Returns the model class
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

def get_embedding_model(model_name: str):
    if model_name == ModelName.text_embedding_ada_002:
        return OpenAIEmbeddings(
            client=None,
            model=ModelName.text_embedding_ada_002,
            chunk_size=1000,
        )
    else:
        raise ValueError("Model name not recognized")
