from langchain.chat_models import ChatOpenAI
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.llms import OpenAI
from langchain import SerpAPIWrapper
from langchain.agents.tools import Tool
from langchain import LLMMathChain

from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.util_models import ModelName

from dotenv import load_dotenv
import os

load_dotenv()


def create_diet_agent():
    """
    Return a PlanAndExecute object for editing a user's diet plan
    """
    search = SerpAPIWrapper(
        search_engine=None,
        serpapi_api_key=os.getenv("SERP_API_KEY"),
    )

    llm = get_model(ModelName.text_davinci_003)

    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
    ]

model = get_model(ModelName.gpt_3_5_turbo)

planner = load_chat_planner(model)

executor = load_agent_executor(model, tools, verbose=True)

agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

if __name__ == "__main__":
    output = agent.run(
        "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
    )
    print(output)
