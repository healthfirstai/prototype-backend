# NOTE: In this file, I'm coding the JSON LLM chain
from langchain import PromptTemplate, OpenAI, LLMChain
from healthfirstai_prototype.util_models import ModelName
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.nutrition_templates import EDIT_JSON_TEMPLATE


def init_edit_json_chain():
    """
    Initialize the edit json chain
    """
    return LLMChain(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        prompt=PromptTemplate(
            input_variables=["agent_input", "user_diet_plan_json"],
            template=EDIT_JSON_TEMPLATE,
        ),
        verbose=True,
    )
