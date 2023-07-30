"""Exercise Chains

This module contains the chains and related functions for the exercise agent feature.
"""

from langchain import PromptTemplate, LLMChain
from healthfirstai_prototype.enums.openai_enums import ModelName
from healthfirstai_prototype.utils import get_model

from .prompts import EDIT_SCHEDULE_JSON_TEMPLATE


def init_edit_schedule_json_chain() -> LLMChain:
    """
    Initialize and configure the Edit JSON chain.

    Returns:
        An instance of the language model chain ready to process the inputs.
    """
    return LLMChain(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        prompt=PromptTemplate(
            input_variables=["agent_input", "user_exercise_schedule_json"],
            template=EDIT_SCHEDULE_JSON_TEMPLATE,
        ),
        verbose=True,
    )
