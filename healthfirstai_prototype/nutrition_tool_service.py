from healthfirstai_prototype.nutrition_chains import run_edit_json_chain
from healthfirstai_prototype.nutrition_utils import (
    get_user_info_dict,
    get_user_meal_plans_as_json,
    get_user_info_for_json_agent,
    get_cached_plan_json,
    get_user_meal_info_json,
)


def get_user_info(user_id: int):
    """
    Given a user ID, query the database and return the user's information.
    """
    return get_user_info_for_json_agent(user_id)


def get_meal(
    user_id: int,
    include_ingredients: bool,
    include_nutrients: bool,
    meal_choice: str,
):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    return get_user_meal_info_json(
        user_id,
        include_ingredients,
        include_nutrients,
        meal_choice,
    )


def edit_diet_plan(agent_input: str, user_id: int):
    """
    Takes a user diet plan and edits it based on the agent input
    """
    run_edit_json_chain(agent_input, user_id)


def get_diet_plan(user_id: int, include_ingredients: bool):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    return get_user_meal_plans_as_json(user_id, include_ingredients)
