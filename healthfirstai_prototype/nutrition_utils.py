import json
from typing import Any
from datetime import date
import redis

from healthfirstai_prototype.database import SessionLocal
from healthfirstai_prototype.datatypes import (
    Food,
    BaseDailyMealPlan,
    CustomDailyMealPlan,
    CustomDailyMealPlanAndMeal,
    DailyMealPlanAndMeal,
    User,
    PersonalizedDailyMealPlan,
    Meal,
    MealIngredient,
    Goal,
    City,
)
from langchain.vectorstores import FAISS
from langchain.schema import Document
from healthfirstai_prototype.util_models import MealChoice, ModelName, MealNames

from healthfirstai_prototype.utils import (
    get_model,
    get_embedding_model,
    connect_to_redis,
)


def create_new_custom_daily_meal_plan():
    # connect to the database
    session = SessionLocal()
    custom_daily_meal_plan = CustomDailyMealPlan()

    # TODO: Change this so that we get the base_daily_meal_plan_id through an algorithm
    base_daily_meal_plan_row = session.query(BaseDailyMealPlan).filter_by(id=1).first()

    if base_daily_meal_plan_row is None:
        print("Error: No base_daily_meal_plan row found.")
        return

    custom_daily_meal_plan.name = base_daily_meal_plan_row.name
    custom_daily_meal_plan.description = base_daily_meal_plan_row.description

    session.add(custom_daily_meal_plan)
    session.commit()
    return custom_daily_meal_plan.id


def insert_into_relationship_table(
    custom_daily_meal_plan_id: int = 1,
    base_daily_meal_plan_id: int = 1,
):
    """
    Insert into many-to-many relationship table for custom_daily_meal_plan and meal
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

    return custom_daily_meal_plan_id


def get_user_info_dict(user_id: int) -> dict[str, Any]:
    """
    Given a user ID, query the database and return all of the user's information
    """
    session = SessionLocal()
    user_info = session.query(User).filter_by(id=user_id).first()
    session.close()
    user_dict = user_info.__dict__
    del user_dict["_sa_instance_state"]
    user_dict["dob"] = user_dict["dob"].isoformat()
    user_dict = dict(sorted(user_dict.items()))
    return user_dict


def get_user_info_for_json_agent(user_id: int) -> str:
    """
    Given a user ID, query the database and return the user's information in a more human-readable format for the JSON agent
    """
    session = SessionLocal()
    o = (
        session.query(User, City, PersonalizedDailyMealPlan, Goal)
        .join(
            City,
            City.id == User.city_id,
        )
        .join(
            PersonalizedDailyMealPlan,
            PersonalizedDailyMealPlan.user_id == User.id,
        )
        .join(
            Goal,
            Goal.id == PersonalizedDailyMealPlan.goal_id,
        )
        .filter(User.id == user_id)
        .all()
    )
    session.close()
    user, user_city, user_meal_plan, user_goal = o[0]  # Get first element of list
    user_dict = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "city_of_residence": user_city.name,
        "age": date.today().year
        - user.dob.year
        - ((date.today().month, date.today().day) < (user.dob.month, user.dob.day)),
        "gender": user.gender,
        "height": f"{str(user.height)}CM",
        "weight": f"{str(user.weight)}KG",
        "goal": user_goal.name,
        "goal_start_date": str(user_meal_plan.start_date),
        "goal_end_date": str(user_meal_plan.end_date),
    }
    return json.dumps(user_dict, indent=2)


def insert_into_personalized_daily_meal_plan(user_id: int):
    """
    Given a user ID, insert a row into the personalized_daily_meal_plan table.
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

    return personalized_daily_meal_plan


def get_user_meal_plans_as_json(
    user_id: int,
    include_ingredients: bool = True,
    meal_choice: str = "",
) -> str:
    """
    Given a user ID, query the database and return the user's meal plan as a JSON object.
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
    # Choose whether to include key nutrients
    # Choose a meal type
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


def cache_diet_plan_redis(user_id: int):
    r = connect_to_redis()
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", get_user_meal_plans_as_json(user_id))


def store_new_diet_plan(user_id: int, new_diet_plan: str):
    r = connect_to_redis()
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", new_diet_plan)


def store_meal(
    user_id: int,
    new_meal: str,
    meal_type: MealNames,
):
    r = connect_to_redis()
    if not (cached_plan := r.hget(f"my-diet-plan:{user_id}", "diet_plan")):
        raise ValueError("No cached plan found for this user.")
    # NOTE: The following two lines will throw an error if the plan + meal is not valid JSON
    cached_plan_dict = json.loads(cached_plan)
    cached_plan_dict[meal_type] = json.loads(new_meal)
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", json.dumps(cached_plan_dict))


def get_cached_plan_json(
    user_id: int,
    include_ingredients: bool = True,
    meal_choice: MealNames = MealNames.all,
):
    r = connect_to_redis()
    if not (cached_plan := r.hget(f"my-diet-plan:{user_id}", "diet_plan")):
        raise ValueError("No cached plan found for this user.")

    cached_plan_dict = json.loads(cached_plan)
    if not include_ingredients:
        if MealNames.breakfast in cached_plan_dict:
            cached_plan_dict[MealNames.breakfast].pop("ingredients", None)
        if MealNames.lunch in cached_plan_dict:
            cached_plan_dict[MealNames.lunch].pop("ingredients", None)
        if MealNames.dinner in cached_plan_dict:
            cached_plan_dict[MealNames.dinner].pop("ingredients", None)
        if MealNames.snack in cached_plan_dict:
            cached_plan_dict[MealNames.snack].pop("ingredients", None)
        if MealNames.drink in cached_plan_dict:
            cached_plan_dict[MealNames.drink].pop("ingredients", None)

    if not meal_choice:
        return json.dumps(cached_plan_dict, indent=2)
    else:
        return json.dumps(cached_plan_dict[meal_choice], indent=2)


# TODO: Store these ranked tools somewhere else. Don't create the vector store every time.
def rank_tools(user_input: str, tools: list):
    vector_store = FAISS.from_documents(
        [
            Document(page_content=t.description, metadata={"index": i})
            for i, t in enumerate(tools)
        ],
        get_embedding_model(ModelName.text_embedding_ada_002),
    )
    docs = vector_store.similarity_search(user_input, k=3)
    return [tools[d.metadata["index"]] for d in docs]


def get_user_meal_info_json(
    user_id: int,
    include_ingredients: bool,
    include_nutrients: bool,
    meal_choice: MealNames,
    cached: bool = False,
):
    """
    Given a user ID, query the database and return the user's diet plan.
    """
    if not cached:
        meal_json = get_user_meal_plans_as_json(
            user_id,
            include_ingredients=True,
            meal_choice=meal_choice,
        )
    else:
        meal_json = get_cached_plan_json(
            user_id,
            include_ingredients=True,
            meal_choice=meal_choice,
        )
    meal_dict = json.loads(meal_json)
    session = SessionLocal()
    if include_nutrients:
        nutrients = {
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
        for ingredient in meal_dict["ingredients"]:
            food = (
                session.query(Food)
                .filter(Food.id == ingredient["ingredient_id"])
                .all()[0]
                .__dict__
            )
            # set values even if they do not exist
            nutrients["calories"] += int(food["Calories"]) if food["Calories"] else 0
            nutrients["fat"] += int(food["Fat_g"]) if food["Fat_g"] else 0
            nutrients["cholesterol"] += (
                int(food["Cholesterol_mg"]) if food["Cholesterol_mg"] else 0
            )
            nutrients["sodium"] += int(food["Sodium_mg"]) if food["Sodium_mg"] else 0
            nutrients["carbs"] += (
                int(food["Carbohydrate_g"]) if food["Carbohydrate_g"] else 0
            )
            nutrients["fiber"] += int(food["Fiber_g"]) if food["Fiber_g"] else 0
            nutrients["sugar"] += int(food["Sugars_g"]) if food["Sugars_g"] else 0
            nutrients["protein"] += int(food["Protein_g"]) if food["Protein_g"] else 0
            nutrients["vitamin_a"] += (
                int(food["Vitamin_A_IU_IU"]) if food["Vitamin_A_IU_IU"] else 0
            )
            nutrients["vitamin_c"] += (
                int(food["Vitamin_C_mg"]) if food["Vitamin_C_mg"] else 0
            )
            nutrients["calcium"] += int(food["Calcium_mg"]) if food["Calcium_mg"] else 0
            nutrients["iron"] += int(food["Iron_Fe_mg"]) if food["Iron_Fe_mg"] else 0

        # Add the convert the nutrition values to strings and add the proper units
        nutrients_with_units = {
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
        meal_dict["nutrients"] = nutrients_with_units
    session.close()
    if not include_ingredients:
        del meal_dict["ingredients"]
    meal_json = json.dumps(meal_dict, indent=2)
    return meal_json


def main():
    pass


if __name__ == "__main__":
    main()
