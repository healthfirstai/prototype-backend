import psycopg2
import json
from datetime import date

from healthfirstai_prototype.database import SessionLocal
from healthfirstai_prototype.datatypes import (
    Food,
    Nutrition_Vector,
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
    base_daily_meal_plan_id=1,
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


def get_user_info_dict(user_id: int) -> dict:
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


def get_user_meal_plans_as_json(user_id: int, include_ingredients: bool = True) -> str:
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
                    # "ingredient_id": ingredient.ingredient_id, # NOTE: We may not need the ID
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
    return json.dumps(meal_plan_dict, indent=2)


def main():
    pass


if __name__ == "__main__":
    main()
