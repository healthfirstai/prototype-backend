# NOTE: This is where the main application logic is implemented for the nutrition agent
import os
import json

from langchain.agents import create_json_agent, AgentExecutor
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec

# NOTE: Using this JSON agent is if the JSON object does not fit in the token window
def start_nutrition_agent(json_string):
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
