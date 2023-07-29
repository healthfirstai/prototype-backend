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
