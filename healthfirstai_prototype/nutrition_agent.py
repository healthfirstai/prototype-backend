import os
import json
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)

from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from healthfirstai_prototype.nutrition_agent_tools import (
    UserInfoTool,
    DietPlanTool,
    EditDietPlanTool,
)
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.util_models import ModelName
from healthfirstai_prototype.nutrition_templates import SYSTEM_PROMPT
import langchain

# langchain.debug = True


def init_agent():
    return initialize_agent(
        tools=[
            DietPlanTool(),
            UserInfoTool(),
            EditDietPlanTool(),
        ],
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )


# NOTE: We will likely not use this
def init_plan_and_execute_diet_agent():
    """
    Return a PlanAndExecute object for editing a user's diet plan
    """
    planner = load_chat_planner(
        llm=get_model(ModelName.gpt_3_5_turbo),
        system_prompt=SYSTEM_PROMPT,
    )

    executor = load_agent_executor(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        tools=[
            UserInfoTool(),
            DietPlanTool(),
            EditDietPlanTool(),
        ],
        verbose=True,
        include_task_in_prompt=True
    )

    return PlanAndExecute(
        planner=planner,
        executor=executor,
        verbose=True,
    )


# NOTE: Using this JSON agent is if the JSON object does not fit in the token window
def start_nutrition_temp_agent(json_string):
    json_dict = json.loads(json_string)[0]
    json_spec = JsonSpec(dict_=json_dict, max_value_length=4000)
    json_toolkit = JsonToolkit(spec=json_spec)

    return create_json_agent(
        llm=OpenAI(
            client=None,
            model="text-davinci-003",
            temperature=0,
        ),
        toolkit=json_toolkit,
        verbose=True,
    )
