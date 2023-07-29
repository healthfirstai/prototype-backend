"""Nutrition Chains

This module contains the chains and related functions for the nutrition agent feature.

Todo:
    * Fix template rendering issue in edit_diet_plan_json
    * Return conversational string that continues confo in edit_diet_plan_json
"""

from langchain import PromptTemplate, LLMChain
from healthfirstai_prototype.enums.openai_enums import ModelName
from healthfirstai_prototype.utils import get_model

from .prompts import EDIT_JSON_TEMPLATE


def init_edit_json_chain() -> LLMChain:
    """
    Initialize and configure the Edit JSON chain.

    Returns:
        An instance of the language model chain ready to process the inputs.
    """
    return LLMChain(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        prompt=PromptTemplate(
            input_variables=["agent_input", "user_diet_plan_json", "meal"],
            template=EDIT_JSON_TEMPLATE,
        ),
        verbose=True,
    )
