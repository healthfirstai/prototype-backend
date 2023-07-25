from healthfirstai_prototype.nutrition_chains import edit_diet_plan_json
from healthfirstai_prototype.util_models import MealNames
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


def get_diet_plan(user_id: int, include_ingredients: bool):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    return get_user_meal_plans_as_json(user_id, include_ingredients)


def get_meal(
    user_id: int,
    include_ingredients: bool,
    include_nutrients: bool,
    meal_choice: MealNames,
    cached: bool,
):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    return get_user_meal_info_json(
        user_id,
        include_ingredients,
        include_nutrients,
        meal_choice,
        cached,
    )


def edit_entire_diet_plan(agent_input: str, user_id: int):
    """
    Takes a user diet plan and edits it based on the agent input
    """
    # TODO: In the future, decide whethere I should or should not include the ingredients
    edit_diet_plan_json(
        agent_input,
        user_id,
        meal_choice=MealNames.all,
        include_ingredients=True,
        store_in_redis=True,
    )


def edit_meal(
    agent_input: str,
    user_id: int,
    meal_choice: MealNames,
    edit_ingredients: bool,
):
    """
    Takes a user diet plan and edits it based on the agent input
    """
    edit_diet_plan_json(
        agent_input,
        user_id,
        meal_choice=meal_choice,
        include_ingredients=edit_ingredients,
        store_in_redis=True,
    )
