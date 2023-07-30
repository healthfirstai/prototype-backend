from langchain.llms import Cohere
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.question_answering import load_qa_chain
from healthfirstai_prototype.enums.openai_enums import ModelName

from healthfirstai_prototype.utils import get_model


def load_chain(chain_type: str = "stuff") -> BaseCombineDocumentsChain:
    """
    This function is loading the chain and sets it up for the agent to use

    Params:
        chain_type (str, optional) : The type of chain to use ("stuff" or "map_reduce")

    Returns:
        The LLM chain object
    """
    return load_qa_chain(
        llm=get_model(ModelName.gpt_3_5_turbo),
        chain_type=chain_type,
        verbose=True,
    )
