# NOTE: In this file, I'm coding the JSON LLM chain
from langchain import PromptTemplate, OpenAI, LLMChain
from healthfirstai_prototype.util_models import ModelName
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.nutrition_templates import JSON_CHAIN_PROMPT

prompt_template = "What is a good name for a company that makes {product}?"

llm = get_model(ModelName.text_davinci_003)
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template),
)
llm_chain("colorful socks")
