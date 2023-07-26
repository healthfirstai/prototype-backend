from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain.schema import BaseMessage
from langchain.llms import Cohere
from langchain.chains import LLMChain

from healthfirstai_prototype.advice_agent import COHERE_API_KEY


# NOTE: this function is not used yet
def set_template(
    height: str,
    weight: str,
    gender: str,
    age: str,
    height_unit: str = "cm",
    weight_unit: str = "kg",
    text: str = "This is a default query.",
) -> list[BaseMessage]:
    """
    This function is setting the template for the chat to use given user's personal information

    Params:
        height (str) : user's height
        weight (str) : user's weight
        gender (str) : user's gender
        age (str) : user's age
        height_unit (str, optional) : user's height unit
        weight_unit (str, optional) : user's weight unit
        text (str, optional) : The user's query / question

    Returns:
        a list of messages using the formatted prompt
    """
    system_message_template = """
    You are a helpful nutrition and exercise assistant that takes into the considerations user's height as {user_height}, 
    user weight as {user_weight}, user's gender as {user_gender}, and user's {user_age} to provide a user with answers to their questions. 
    If you don't have a specific answer, just say I don't know, and do not make anything up.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_message_template
    )

    human_template = text
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    return chat_prompt.format_prompt(
        user_height=height + " " + height_unit,
        user_weight=weight + " " + weight_unit,
        user_gender=gender,
        user_age=age + " years old",
    ).to_messages()


def template_to_assess_search_results(
    google_search_result: str = "",
    faiss_search_result: str = "",
    prompt: str = "",
) -> str:
    """
    This function is used to assess the outputs from the two search engines

    Params:
        google_search_result (str, optional) : The response from the SerpAPI's query to Google
        faiss_search_result (str, optional) : The response from the LLM chain object
        prompt (str, optional) : The user's query / question

    Returns:
        a list of messages using the formatted prompt
    """
    system_message_template = """\
    You are a helpful assistant which helps to assess the relevance of the Google search result: {google_search_result}, and the knowledge base search result: {faiss_search_result} regarding the following prompt / question: {prompt}. 
    Please look at both of the search results regarding the prompt I gave you, and return to me that particular result without modifying it. If you think they are both good enough, please return the knowledge base search result, otherwise return the Google search result. 
    Do not make anything up.
    """

    system_message_prompt = PromptTemplate.from_template(system_message_template)

    return system_message_prompt.format(
        google_search_result=google_search_result,
        faiss_search_result=faiss_search_result,
        prompt=prompt,
    )


def run_assessment_chain(prompt_template: str) -> str:
    """
    This function is used to run the assessment chain which is simply a single chain object powered
    by the LLM which is supposed to check the relevance of the search results from the two different search methods
    and provide us with the best result.

    Params:
        prompt_template (str): The template for the assessment chain will use

    Returns:
        (str): The response from the LLM chain object
    """
    llm = Cohere(
        cohere_api_key=COHERE_API_KEY,
        temperature=0,
        verbose=False,
        model="command-light",
    )  # type: ignore
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)  # type: ignore
    response = llm_chain.run()
    return response
