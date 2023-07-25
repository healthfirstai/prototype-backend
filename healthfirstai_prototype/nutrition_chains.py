# NOTE: In this file, I'm coding the JSON LLM chain
from langchain import PromptTemplate, OpenAI, LLMChain
from healthfirstai_prototype.util_models import ModelName
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.nutrition_templates import EDIT_JSON_TEMPLATE
from healthfirstai_prototype.nutrition_utils import get_cached_plan_json, store_new_diet_plan
import redis


# TODO: This is WAY too slow. I need it to only replace certain keys
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


def run_edit_json_chain(agent_input: str, user_id: int):
    user_diet_plan_json = get_cached_plan_json(user_id)
    new_diet_plan = init_edit_json_chain().predict(
        agent_input=agent_input,
        user_diet_plan_json=user_diet_plan_json,
    )
    store_new_diet_plan(user_id, new_diet_plan)
    return "Successfully updated your diet plan!"
