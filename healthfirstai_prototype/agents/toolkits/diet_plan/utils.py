"""Diet Plan Utility Functions

This module contains the logic for the nutrition feature.

Todo:
    * Move some of this logic out of this file and into a general conttoller file. It has nothing to do with the agent itself.
"""

import json
from typing import Any

from langchain.agents.tools import BaseTool

from healthfirstai_prototype.enums.meal_enums import MealNames
from .chains import init_edit_json_chain
from healthfirstai_prototype.enums.openai_enums import ModelName
from healthfirstai_prototype.models.database import SessionLocal
from healthfirstai_prototype.models.data_models import (
    Food,
    BaseDailyMealPlan,
    CustomDailyMealPlan,
    CustomDailyMealPlanAndMeal,
    DailyMealPlanAndMeal,
    User,
    PersonalizedDailyMealPlan,
    Meal,
    MealIngredient,
)

from langchain.vectorstores import FAISS
from langchain.schema import Document

from healthfirstai_prototype.utils import (
    get_embedding_model,
    connect_to_redis,
)


def create_new_custom_daily_meal_plan() -> None:
    """
    Create a new custom_daily_meal_plan row in the database

    Raises:
        ValueError: If no base_daily_meal_plan row is found

    Todo:
        Change this so that we get the base_daily_meal_plan_id through an algorithm
    """
    # connect to the database
    session = SessionLocal()
    custom_daily_meal_plan = CustomDailyMealPlan()

    base_daily_meal_plan_row = session.query(BaseDailyMealPlan).filter_by(id=1).first()

    if base_daily_meal_plan_row is None:
        raise ValueError("No base_daily_meal_plan row found.")

    custom_daily_meal_plan.name = base_daily_meal_plan_row.name
    custom_daily_meal_plan.description = base_daily_meal_plan_row.description

    session.add(custom_daily_meal_plan)
    session.commit()


def insert_into_relationship_table(
        custom_daily_meal_plan_id: int = 1,
        base_daily_meal_plan_id: int = 1,
) -> None:
    """
    Insert into many-to-many relationship table for custom_daily_meal_plan and meal

    Args:
        custom_daily_meal_plan_id: The ID of the newly created custom_daily_meal_plan row
        base_daily_meal_plan_id: The ID of the base_daily_meal_plan row
    """
    session = SessionLocal()

    daily_meal_plan_and_meal_rows = (
        session.query(DailyMealPlanAndMeal)
        .filter_by(base_daily_meal_plan_id=base_daily_meal_plan_id)
        .all()
    )

    for daily_meal_plan_and_meal_row in daily_meal_plan_and_meal_rows:
        item = CustomDailyMealPlanAndMeal(
            custom_daily_meal_plan_id=custom_daily_meal_plan_id,
            meal_id=daily_meal_plan_and_meal_row.meal_id,
        )
        session.add(item)
        session.commit()


def get_user_info_dict(user_id: int) -> dict[str, Any]:
    """
    Given a user ID, query the database and return the user's information in a dictionary

    Args:
        user_id: The ID of the user

    Returns:
        A dictionary containing the user's information
    """
    session = SessionLocal()
    user_info = session.query(User).filter_by(id=user_id).first()
    session.close()
    user_dict = user_info.__dict__
    del user_dict["_sa_instance_state"]
    user_dict["dob"] = user_dict["dob"].isoformat()
    user_dict = dict(sorted(user_dict.items()))
    return user_dict


def insert_into_personalized_daily_meal_plan(user_id: int) -> None:
    """
    Insert into personalized_daily_meal_plan table

    Args:
        user_id: The ID of the user

    Returns:
        None
    """
    session = SessionLocal()
    personalized_daily_meal_plan = PersonalizedDailyMealPlan(
        user_id=user_id,
        custom_daily_meal_plan=1,
        start_date="2020-01-01",
        end_date="2021-02-01",
        goal_id=1,
    )
    session.add(personalized_daily_meal_plan)
    session.commit()
    session.close()


# TODO: Refactor this function
def get_user_meal_plans_as_json(
        user_id: int,
        include_ingredients: bool = True,
        meal_choice: str = "",
) -> str:
    """
    Given a user ID, query the database and return the user's meal plans in a JSON string

    Args:
        user_id: The ID of the user
        include_ingredients: Whether to include the ingredients in the JSON string
        meal_choice: The meal choice (breakfast, lunch, dinner, snack)

    Returns:
        str: A JSON string containing the user's meal plans
    """
    session = SessionLocal()
    personalized_daily_meal_plans = (
        session.query(PersonalizedDailyMealPlan, CustomDailyMealPlan)
        .join(
            CustomDailyMealPlan,
            PersonalizedDailyMealPlan.custom_daily_meal_plan == CustomDailyMealPlan.id,
        )
        .filter(PersonalizedDailyMealPlan.user_id == user_id)
        .all()
    )

    meal_plan_dict = {}
    for (
            personalized_daily_meal_plan,
            custom_daily_meal_plan,
    ) in personalized_daily_meal_plans:
        meal_ids = (
            session.query(CustomDailyMealPlanAndMeal.meal_id)
            .filter(
                CustomDailyMealPlanAndMeal.custom_daily_meal_plan_id
                == custom_daily_meal_plan.id
            )
            .all()
        )
        meal_ids = [meal_id[0] for meal_id in meal_ids]
        meals = session.query(Meal).filter(Meal.id.in_(meal_ids)).all()
        custom_daily_meal_plan_dict = {
            "id": custom_daily_meal_plan.id,
            "name": custom_daily_meal_plan.name,
            "description": custom_daily_meal_plan.description,
        }
        for meal in meals:
            ingredients = (
                session.query(MealIngredient, Food)
                .join(Food, MealIngredient.ingredient_id == Food.id)
                .filter(MealIngredient.meal_id == meal.id)
                .all()
            )
            ingredient_list = [
                {
                    "ingredient_id": ingredient.ingredient_id,  # NOTE: We may not need the ID
                    "food_name": food.Name,
                    "unit_of_measurement": ingredient.unit_of_measurement,
                    "quantity": ingredient.quantity,
                }
                for (ingredient, food) in ingredients
            ]
            custom_daily_meal_plan_dict[str(meal.meal_type)] = {
                "id": meal.id,
                "name": meal.name,
                "description": meal.description,
            }
            if include_ingredients:
                custom_daily_meal_plan_dict[str(meal.meal_type)][
                    "ingredients"
                ] = ingredient_list
        meal_plan_dict = (
            {
                "id": personalized_daily_meal_plan.id,
                "custom_daily_meal_plan": custom_daily_meal_plan_dict,
            },
        )
    session.close()
    if meal_choice == MealNames.breakfast:
        meal_plan_dict = meal_plan_dict[0]["custom_daily_meal_plan"][
            MealNames.breakfast
        ]
    elif meal_choice == MealNames.lunch:
        meal_plan_dict = meal_plan_dict[0]["custom_daily_meal_plan"][MealNames.lunch]
    elif meal_choice == MealNames.dinner:
        meal_plan_dict = meal_plan_dict[0]["custom_daily_meal_plan"][MealNames.dinner]
    elif meal_choice == MealNames.snack:
        meal_plan_dict = meal_plan_dict[0]["custom_daily_meal_plan"][MealNames.snack]
    elif meal_choice == MealNames.drink:
        meal_plan_dict = meal_plan_dict[0]["custom_daily_meal_plan"][MealNames.drink]
    else:
        meal_plan_dict = meal_plan_dict[0]["custom_daily_meal_plan"]
    return json.dumps(meal_plan_dict, indent=2)


def cache_diet_plan_redis(user_id: int) -> None:
    """
    Cache the user's diet plan in Redis

    Args:
        user_id: The ID of the user
    """
    r = connect_to_redis()
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", get_user_meal_plans_as_json(user_id))


def store_new_diet_plan(user_id: int, new_diet_plan: str) -> None:
    """
    Store a new diet plan for the user

    Args:
        user_id: The ID of the user
        new_diet_plan: The new diet plan JSON string to store
    """
    r = connect_to_redis()
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", new_diet_plan)


def store_meal(user_id: int, new_meal: str, meal_type: MealNames) -> None:
    """
    Store a new meal in the user's diet plan

    Args:
        user_id: The ID of the user
        new_meal: The new meal to store
        meal_type: The type of meal (breakfast, lunch, dinner, snack)
    """
    r = connect_to_redis()
    if not (cached_plan := r.hget(f"my-diet-plan:{user_id}", "diet_plan")):
        raise ValueError("No cached plan found for this user.")
    cached_plan_dict = json.loads(cached_plan)  # Throws error if not valid JSON
    cached_plan_dict[meal_type] = json.loads(new_meal)  # Throws error if not valid JSON
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", json.dumps(cached_plan_dict))


def get_cached_plan_json(
        user_id: int,
        include_ingredients: bool = True,
        meal_choice: MealNames = MealNames.all,
):
    """
    Get the cached diet plan for the user

    Args:
        user_id: The ID of the user
        include_ingredients: Whether to include the ingredients in the response
        meal_choice: The meal to return (breakfast, lunch, dinner, snack, all)
    """
    r = connect_to_redis()
    if not (cached_plan := r.hget(f"my-diet-plan:{user_id}", "diet_plan")):
        raise ValueError("No cached plan found for this user.")

    cached_plan_dict = json.loads(cached_plan)
    if not include_ingredients:
        for meal in MealNames:
            if meal in cached_plan_dict:
                cached_plan_dict[meal].pop("ingredients", None)

    if not meal_choice:
        return json.dumps(cached_plan_dict, indent=2)
    else:
        return json.dumps(cached_plan_dict[meal_choice], indent=2)


def rank_tools(user_input: str, tools: list[BaseTool], k=3) -> list[BaseTool]:
    """
    Rank the tools tools list based on the user's input.
    Returns the top k tools as a list for the agent

    Returns:
        A list of the top k tools.

    Todo:
        * Store the vector store somewhere else. Don't create it every time.
    """
    vector_store = FAISS.from_documents(
        [
            Document(page_content=t.description, metadata={"index": i})
            for i, t in enumerate(tools)
        ],
        get_embedding_model(ModelName.text_embedding_ada_002),
    )
    docs = vector_store.similarity_search(user_input, k=k)
    return [tools[d.metadata["index"]] for d in docs]


def format_nutrients_with_units(nutrients: dict[str, int]) -> dict[str, str]:
    """
    Format the nutrients by adding the units.

    Args:
        nutrients: A dictionary of the nutrients and their amounts.

    Returns:
        A dictionary of the nutrients with their units.
    """
    return {
        "calories": str(nutrients["calories"]) + " kcal",
        "fat": str(nutrients["fat"]) + " g",
        "cholesterol": str(nutrients["cholesterol"]) + " mg",
        "sodium": str(nutrients["sodium"]) + " mg",
        "carbs": str(nutrients["carbs"]) + " g",
        "fiber": str(nutrients["fiber"]) + " g",
        "sugar": str(nutrients["sugar"]) + " g",
        "protein": str(nutrients["protein"]) + " g",
        "vitamin_a": str(nutrients["vitamin_a"]) + " IU",
        "vitamin_c": str(nutrients["vitamin_c"]) + " mg",
        "calcium": str(nutrients["calcium"]) + " mg",
        "iron": str(nutrients["iron"]) + " mg",
    }


def create_nutrient_dict() -> dict[str, int]:
    """
    Create a dictionary of selected key nutrients and initialize their values to 0.

    Returns:
        A dictionary of the nutrients and their values.
    """
    return {
        "calories": 0,
        "fat": 0,
        "cholesterol": 0,
        "sodium": 0,
        "carbs": 0,
        "fiber": 0,
        "sugar": 0,
        "protein": 0,
        "vitamin_a": 0,
        "vitamin_c": 0,
        "calcium": 0,
        "iron": 0,
    }


def update_nutrient_values(
        food: dict[str, Any],
        nutrients: dict[str, int],
) -> dict[str, int]:
    """
    Update nutrient values based on the information in the food item.

    Args:
        food: A dictionary representing a food item with nutrient information.
        nutrients: The current nutrient values.

    Returns:
        The updated nutrient values.
    """
    nutrient_names = [
        ("Calories", "calories"),
        ("Fat_g", "fat"),
        ("Cholesterol_mg", "cholesterol"),
        ("Sodium_mg", "sodium"),
        ("Carbohydrate_g", "carbs"),
        ("Fiber_g", "fiber"),
        ("Sugars_g", "sugar"),
        ("Protein_g", "protein"),
        ("Vitamin_A_IU_IU", "vitamin_a"),
        ("Vitamin_C_mg", "vitamin_c"),
        ("Calcium_mg", "calcium"),
        ("Iron_Fe_mg", "iron"),
    ]
    for food_key, nutrient_key in nutrient_names:
        nutrient_value = food.get(food_key)
        nutrients[nutrient_key] += int(nutrient_value) if nutrient_value else 0

    return nutrients


# TODO: Create meal to meal + ingredient mapping
def get_user_meal_info_json(
        user_id: int,
        include_ingredients: bool,
        include_nutrients: bool,
        meal_choice: MealNames,
        cached: bool = False,
) -> str:
    """
    Given a user ID, query the database and return the user's diet plan.

    Args:
        user_id: The ID of the user
        include_ingredients: Whether to include the ingredients in the response
        include_nutrients: Whether to include the nutrients in the response
        meal_choice: The meal to return
        cached: Whether to use the cached plan

    Returns:
        A JSON string representing the user's diet plan

    Todo:
        * Break this up into smaller functions in a project-wide refactor
    """
    get_meal_func = get_cached_plan_json if cached else get_user_meal_plans_as_json
    meal_json = get_meal_func(
        user_id,
        include_ingredients=True,
        meal_choice=meal_choice,
    )
    meal_dict = json.loads(meal_json)
    print(meal_dict)
    if include_nutrients:
        nutrients = create_nutrient_dict()
        for ingredient in meal_dict["ingredients"]:
            food = get_food_by_ingredient_id(ingredient["ingredient_id"])
            nutrients = update_nutrient_values(food, nutrients)
        meal_dict["nutrients"] = format_nutrients_with_units(nutrients)
    if not include_ingredients:
        del meal_dict["ingredients"]
    meal_json = json.dumps(meal_dict, indent=2)
    return meal_json


def get_food_by_ingredient_id(ingredient_id: int) -> dict[str, Any]:
    """
    Query the database to get food by ingredient_id.

    Args:
        ingredient_id: The ID of the ingredient
        session: The session for database query

    Returns:
        A dict of food information.
    """
    session = SessionLocal()
    output = session.query(Food).filter(Food.id == ingredient_id).first().__dict__
    session.close()
    return output


def get_diet_plan(user_id: int, include_ingredients: bool):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    return get_cached_plan_json(user_id, include_ingredients)


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
    # TODO: In the future, decide whether I should or should not include the ingredients
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
    return edit_diet_plan_json(
        agent_input,
        user_id,
        meal_choice=meal_choice,
        include_ingredients=edit_ingredients,
        store_in_redis=True,
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

    Args:
        agent_input: The agent's input text for the conversation.
        user_id: The ID of the user.
        meal_choice: The meal choice to edit.
        include_ingredients: Whether to include the ingredients in the diet plan.
        store_in_redis: Whether to store the new diet plan in Redis.

    Returns:
        The new diet plan JSON.
    """
    if meal_choice == MealNames.all:
        # TODO: When an edit is made, have the LLM chain extract the meal ingredients
        # Insert the meal ingredients into redis as well
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
            # TODO: Adjust this function that it shows the meal_choice properly in the prompt
            meal=meal_choice,
        )
        if store_in_redis:
            store_meal(user_id, new_meal, meal_choice)
    # TODO: Make sure that the return value "continues the conversation" and lets the conversation agent know about
    #  the new changes
    meal_name = meal_choice or "diet_plan"
    return f"Your {meal_name} has been updated successfully.\nHere is your new {meal_name}:\n{new_meal}"
