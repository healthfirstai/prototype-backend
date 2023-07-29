import json
from datetime import date
from healthfirstai_prototype.models.database import SessionLocal
from healthfirstai_prototype.models.data_models import (
    User,
    PersonalizedDailyMealPlan,
    Goal,
    City,
)


def get_user_info_for_json_agent(user_id: int) -> str:
    """
    Given a user ID, query the database and return the user's information in a JSON string

    Args:
        user_id: The ID of the user

    Returns:
        A JSON string containing the user's information

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


def get_user_info(user_id: int):
    """
    Given a user ID, query the database and return the user's information.
    """
    return get_user_info_for_json_agent(user_id)
