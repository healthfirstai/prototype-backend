# NOTE: Here, I'm going to query the PostGres database and generate JSON from the results.
#       This will be used to generate the JSON for the front-end.

import psycopg2
import json

if __name__ == "__main__":
    from database import SessionLocal
    from datatypes import (
        Food,
        Nutrition_Vector,
        BaseDailyMealPlan,
        CustomDailyMealPlan,
        CustomDailyMealPlanAndMeal,
        DailyMealPlanAndMeal,
        User,
        PersonalizedDailyMealPlan,
    )
else:
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
    )


def create_new_custom_daily_meal_plan():
    # connect to the database
    session = SessionLocal()
    custom_daily_meal_plan = CustomDailyMealPlan()

    # TODO: Change this so that it's not hard-coded
    base_daily_meal_plan_row = session.query(BaseDailyMealPlan).filter_by(id=1).first()

    # Set the values of the custom_daily_meal_plan instance based on the replicated row
    if base_daily_meal_plan_row is None:
        print("Error: No base_daily_meal_plan row found.")
        return

    custom_daily_meal_plan.name = base_daily_meal_plan_row.name
    custom_daily_meal_plan.description = base_daily_meal_plan_row.description

    # Add the custom_daily_meal_plan instance to the session and commit the changes
    session.add(custom_daily_meal_plan)
    session.commit()
    return custom_daily_meal_plan.id


def insert_into_relationship_table(custom_daily_meal_plan_id: int = 1):
    session = SessionLocal()

    daily_meal_plan_and_meal_rows = (
        session.query(DailyMealPlanAndMeal).filter_by(base_daily_meal_plan_id=1).all()
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


# insert a user and generate a diet plan
# Given a user ID, query the database and generate a diet plan in the form of a JSON string
def get_started(id: int):
    pass

def get_user_plan(id: int):
    pass


def main():
    # insert_into_relationship_table()
    insert_into_personalized_daily_meal_plan(get_user_info(1))


if __name__ == "__main__":
    main()
