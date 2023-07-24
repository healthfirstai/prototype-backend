import json
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.memory import (
    RedisChatMessageHistory,
    ConversationTokenBufferMemory,
)
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.llms.openai import OpenAI
from langchain.tools.json.tool import JsonSpec
from healthfirstai_prototype.nutrition_agent_tools import (
    UserInfoTool,
    DietPlanTool,
    EditDietPlanTool,
)
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.util_models import ModelName
from healthfirstai_prototype.nutrition_templates import (
    SYSTEM_PROMPT,
    DIET_AGENT_PROMPT_TEMPLATE,
)
import langchain

# NOTE: Imports for new agent
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain import (
    OpenAI,
)
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

langchain.debug = False


def init_agent(user_input: str, user_id: int = 1, session_id="my-session"):
    tools = [
        DietPlanTool(),
        UserInfoTool(),
        EditDietPlanTool(),
    ]
    message_history = RedisChatMessageHistory(session_id=session_id)

    memory = ConversationTokenBufferMemory(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        chat_memory=message_history,
        max_token_limit=2000,
    )

    history = memory.load_memory_variables({"input": user_input}).get("history")
    prompt = OpenAIFunctionsAgent.create_prompt(
        SystemMessage(
            content=DIET_AGENT_PROMPT_TEMPLATE.format(
                history=history,
                user_id=user_id,
            )
        )
    )
    agent = OpenAIFunctionsAgent(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        tools=tools,
        prompt=prompt,
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=False,
        memory=memory,
    )


def init_new_agent(user_input: str, session_id="other-session", user_id: int = 1):
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    message_history = RedisChatMessageHistory(session_id=session_id)
    memory = ConversationTokenBufferMemory(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        memory_key="memory",
        chat_memory=message_history,
        max_token_limit=2000,
        return_messages=True,
    )

    llm = get_model(ModelName.gpt_3_5_turbo_0613)
    tools = [
        DietPlanTool(),
        UserInfoTool(),
        EditDietPlanTool(),
    ]
    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
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
        include_task_in_prompt=True,
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
