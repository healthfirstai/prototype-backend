from abc import ABC
from typing import Type

from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from healthfirstai_prototype.models.database import OPENAI_API_KEY
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

# Create a tool that queries the database and returns the answer



