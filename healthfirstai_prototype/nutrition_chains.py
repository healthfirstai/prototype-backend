from langchain import PromptTemplate, OpenAI, LLMChain
from healthfirstai_prototype.util_models import ModelName, MealNames
from healthfirstai_prototype.utils import get_model
from healthfirstai_prototype.nutrition_templates import EDIT_JSON_TEMPLATE
from healthfirstai_prototype.nutrition_utils import (
    get_cached_plan_json,
    store_new_diet_plan,
    store_meal,
)


def init_edit_json_chain():
    """
    Initialize and configure the Edit JSON chain.

    Returns:
        LLMChain: An instance of the language model chain ready to process the inputs.
    """
    return LLMChain(
        llm=get_model(ModelName.gpt_3_5_turbo_0613),
        prompt=PromptTemplate(
            input_variables=["agent_input", "user_diet_plan_json", "meal"],
            template=EDIT_JSON_TEMPLATE,
        ),
        verbose=True,
    )


def edit_diet_plan_json(
    agent_input: str,
    user_id: int,
    meal_choice: MealNames = MealNames.all,
    include_ingredients: bool = True,
    store_in_redis: bool = True,
) -> str:
    """
    Run the Edit JSON chain with the provided agent's input and the user's ID.

    Parameters:
        agent_input (str): The agent's input text for the conversation.
        user_id (int): The ID of the user.
        meal_choice (str): The meal choice to edit.
        include_ingredients (bool): Whether to include the ingredients in the meal plan.
        store_in_cache (bool): Whether to store the new meal plan in the cache.

    Returns:
        confirmation_message (str): A success message indicating the diet plan was updated successfully.
    """
    if meal_choice == MealNames.all:
        new_meal = init_edit_json_chain().predict(
            agent_input=agent_input,
            user_diet_plan_json=get_cached_plan_json(
                user_id,
                meal_choice=MealNames.all,
                include_ingredients=include_ingredients,
            ),
            meal="diet",
        )
        if store_in_redis:
            store_new_diet_plan(user_id, new_meal)
    else:
        new_meal = init_edit_json_chain().predict(
            agent_input=agent_input,
            user_diet_plan_json=get_cached_plan_json(
                user_id,
                meal_choice=meal_choice,
                include_ingredients=include_ingredients,
            ),
            # TODO: For some reason the prompt is not showing meal_choice properly
            meal=meal_choice,
        )
        if store_in_redis:
            store_meal(user_id, new_meal, meal_choice)
    # TODO: Make sure that the return value "continues the conversation"
    return "Your diet plan has been updated successfully."
