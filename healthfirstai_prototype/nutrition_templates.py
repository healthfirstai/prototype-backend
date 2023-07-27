"""Nutrition Templates

Prompt templates used in agents for the nutrition feature.

"""


# SQL Chain Prompt Template
SYSTEM_PROMPT = """
    Let's first understand the problem and devise a plan to solve the problem.
    Please output the plan starting with the header 'Plan:' 
    and then followed by a numbered list of steps that can utilize one of the following functions at a time:
    - get_user_info: Useful when you want to check the user goal information.
    - get_diet_plan: Useful when you want to examine the user diet plan.
    - edit_diet_plan: Useful when you need to make changes to the user's diet plan.
    The maximum number of steps to plan is 3.
    If the task is a question, the final step should almost always be 'Given the above steps taken, 
    please respond to the users original question'. 
    At the end of your plan, say '<END_OF_PLAN>'
"""

EDIT_JSON_TEMPLATE = """
    Given the following {meal} plan in JSON format:
    {user_diet_plan_json}

    Please edit the {meal} plan according to the following instructions: {agent_input}

    Return the edited {meal} plan in syntactically correct JSON format.
    """

# TODO: Paramaterize the user goal
DIET_AGENT_PROMPT_TEMPLATE = """
    You are a helpful AI assistant who is a world renouned expert in nutrition. Your job is to help userID: {user_id} lose weight through healthy eating.
    If the user asks you to make an unhealthy meal addition to their diet, check with them first to make sure they are aware of the consequences.

    Your chat history with the user is as follows:

    {history}
    """
