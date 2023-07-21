import psycopg2
import json

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


def get_user_info(user_id: int):
    """
    Given a user ID, query the database and return the user's information.
    """
    session = SessionLocal()
    user_info = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user_info


def insert_into_personalized_daily_meal_plan(user_info: User):
    """
    Given a user ID, insert a row into the personalized_daily_meal_plan table.
    """
    session = SessionLocal()
    personalized_daily_meal_plan = PersonalizedDailyMealPlan(
        user_id=user_info.id,
        custom_daily_meal_plan=1,
        start_date="2020-01-01",
        end_date="2021-02-01",
        goal_id=1,
    )
    session.add(personalized_daily_meal_plan)
    session.commit()
    session.close()

    return personalized_daily_meal_plan


def get_user_meal_plans(user_id: int) -> str:
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
                "ingredients": ingredient_list,
            }
        meal_plan_dict = (
            {
                "id": personalized_daily_meal_plan.id,
                "start_date": str(personalized_daily_meal_plan.start_date),
                "end_date": str(personalized_daily_meal_plan.end_date),
                # "goal_id": personalized_daily_meal_plan.goal_id,
                "goal_id": personalized_daily_meal_plan.goal_id,
                "custom_daily_meal_plan": custom_daily_meal_plan_dict,
            },
        )
    session.close()
    return json.dumps(meal_plan_dict, indent=2)


def main():
    # insert_into_relationship_table()
    insert_into_personalized_daily_meal_plan(get_user_info(1))


if __name__ == "__main__":
    main()
