"""Chat Agent

This module contains the functions for initializing the chat agent and the PlanAndExecute object for editing a user's diet plan.

"""
from langchain.memory import (
    RedisChatMessageHistory,
    ConversationTokenBufferMemory,
)
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.agents.agent_types import AgentType

from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.enums.openai_enums import ModelName
from healthfirstai_prototype.models.database import sql_agent_db
from langchain.schema import SystemMessage
from .toolkits.diet_plan.tools import (
    GetUserInfoTool,
    DietPlanTool,
    EditDietPlanTool,
    EditBreakfastTool,
    EditLunchTool,
    EditDinnerTool,
    BreakfastTool,
    LunchTool,
    DinnerTool,
)
from .toolkits.diet_plan.utils import rank_tools
from .toolkits.diet_plan.prompts import DIET_AGENT_PROMPT_TEMPLATE # TODO: Make this a general template used by the chat_agent
import langchain


langchain.debug = False


def init_chat_agent(
    user_input: str,
    user_id: int = 1,
    session_id="my-session",
    verbose=True,
) -> AgentExecutor:
    """
    Initialize and configure the conversation agent with the provided user input.

    Parameters:
        user_input (str): The user's input text for the conversation.
        user_id (int, optional): The ID of the user. Default is 1.
        session_id (str, optional): The session ID for maintaining conversation history. Default is "my-session".

    Returns:
        AgentExecutor: An instance of the conversation agent executor ready to handle user interactions.
    """
    # NOTE: Hook into callbacks in the future with callbacks=[HumanApprovalCallbackHandler()]
    tools = [
        DietPlanTool(),
        GetUserInfoTool(),
        EditDietPlanTool(),
        EditBreakfastTool(),
        EditLunchTool(),
        EditDinnerTool(),
        BreakfastTool(),
        LunchTool(),
        DinnerTool(),
    ]
    tools = rank_tools(user_input, tools)
    message_history = RedisChatMessageHistory(session_id=session_id)

    memory = ConversationTokenBufferMemory(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        chat_memory=message_history,
        max_token_limit=500,
    )

    history = memory.load_memory_variables({"input": user_input}).get("history")
    prompt = OpenAIFunctionsAgent.create_prompt(
        SystemMessage(
            content=DIET_AGENT_PROMPT_TEMPLATE.format(
                history=history,
                user_id=user_id,
                user_goal="lose weight",  # TODO: Parameterize this in the future
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
        verbose=verbose,
        memory=memory,
    )


def init_sql_agent() -> AgentExecutor:
    return create_sql_agent(
        llm=get_model(ModelName.text_davinci_003),
        toolkit=SQLDatabaseToolkit(
            db=sql_agent_db,
            llm=get_model(ModelName.text_davinci_003),
        ),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


def init_openai_func_sql_agent() -> AgentExecutor:
    return create_sql_agent(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        toolkit=SQLDatabaseToolkit(
            db=sql_agent_db,
            llm=get_model(ModelName.text_davinci_003),
        ),
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )


# TODO: Add the ability to track the token usage of the agent and the corresponding cost
# Tally this and track it for a conversation
