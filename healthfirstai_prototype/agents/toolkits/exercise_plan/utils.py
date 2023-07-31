import json
from typing import Optional
from healthfirstai_prototype.enums.exercise_enums import DaysOfTheWeek

from healthfirstai_prototype.models.exercise_data_models import (
    ExerciseType,
    BodyPart,
    Difficulty,
    Equipment,
    Exercise,
    UserWorkoutSchedule,
    Workout,
    WorkoutExercise,
)
from .chains import init_edit_schedule_json_chain
from healthfirstai_prototype.models.database import SessionLocal

from healthfirstai_prototype.utils import connect_to_redis


def get_workout_schedule_json(user_id: int) -> str:
    """
    Get the user's workout schedule in JSON format

    Args:
        user_id: The ID of the user

    Returns:
        The user's workout schedule in JSON format
    """
    session = SessionLocal()

    try:
        return extract_workout_data(session, user_id)
    except Exception as e:
        raise e

    finally:
        # Close the session when done
        session.close()


def extract_workout_data(session, user_id: int) -> str:
    """
    Extract the user's workout schedule data from the database
    """
    # Query to fetch the user's schedule along with workout details
    user_schedules = session.query(UserWorkoutSchedule).filter_by(user_id=user_id).all()

    # Initialize the schedule dictionary
    schedule_json = {}

    for user_schedule in user_schedules:
        schedule_id = user_schedule.schedule_id
        schedule_day = user_schedule.schedule_day
        schedule_time = user_schedule.schedule_time
        workout_id = user_schedule.workout_id
        workout = session.query(Workout).filter_by(workout_id=workout_id).first()

        exercise_dict = {}
        workout_exercises = (
            session.query(WorkoutExercise)
            .filter_by(workout_id=workout_id)
            .join(Exercise)
            .join(ExerciseType)
            .join(BodyPart)
            .all()
        )
        if workout is None:
            raise ValueError(f"Exercise with exercise_id {workout_id} does not exist")

        for workout_exercise in workout_exercises:
            exercise_id = workout_exercise.exercise_id
            exercise = (
                session.query(Exercise).filter_by(exercise_id=exercise_id).first()
            )
            if exercise is None:
                raise ValueError(
                    f"Exercise with exercise_id {exercise_id} does not exist"
                )
            exercise_type = (
                session.query(ExerciseType.exercise_type)
                .filter_by(exercise_type_id=exercise.exercise_type_id)
                .scalar()
            )
            body_parts = (
                session.query(BodyPart.bodypart_name)
                .filter_by(bodypart_id=exercise.bodypart_id)
                .scalar()
            )
            difficulty = (
                session.query(Difficulty.difficulty_name)
                .filter_by(difficulty_id=exercise.difficulty_id)
                .scalar()
            )
            equipment = (
                session.query(Equipment.equipment_name)
                .filter_by(equipment_id=exercise.equipment_id)
                .scalar()
            )

            exercise_info = {
                "exercise_id": exercise_id,
                "name": exercise.name,
                "description": exercise.description,
                "exercise_type": exercise_type,
                "equipment": equipment,
                "difficulty": difficulty,
                "body_part": body_parts,
                "reps": workout_exercise.reps,
                "sets": workout_exercise.sets,
            }
            exercise_dict[exercise_id] = exercise_info

            schedule_info = {
                "schedule_time": str(schedule_time),
                "workout_name": workout.workout_name,
                "workout_description": workout.workout_description,
                "exercises": list(exercise_dict.values()),
            }

            schedule_json[schedule_day] = schedule_info
    return json.dumps(schedule_json, indent=2)


def cache_workout_schedule_redis(user_id: int) -> int:
    """
    Cache the user's diet plan in Redis

    Args:
        user_id: The ID of the user
    """
    r = connect_to_redis()
    return r.hset(
        f"my-workout-schedule:{user_id}",
        "workout_schedule",
        get_workout_schedule_json(user_id),
    )


def store_new_workout(
    user_id: int,
    new_workout: str,
    day_of_the_week: DaysOfTheWeek,
) -> None:
    """
    Store the new workout schedule in Redis

    Args:
        user_id: The ID of the user
        new_workout: The new workout schedule
        day_of_the_week: The day of the week to store the workout schedule for
    """
    r = connect_to_redis()
    if not (cached_workout := r.hget(f"my-workout-schedule:{user_id}", "workout_schedule")):
        raise ValueError("No cached workout schedule found for this user.")
    cached_workout_dict = json.loads(cached_workout)  # Throws error if not valid JSON
    cached_workout_dict[day_of_the_week] = json.loads(new_workout)  # Throws error if not valid JSON
    r.hset(f"my-diet-plan:{user_id}", "diet_plan", json.dumps(cached_workout_dict))


def store_new_workout_schedule_json(
    user_id: int,
    new_schedule: str,
) -> None:
    """
    Store the new workout schedule in Redis

    Args:
        user_id: The ID of the user
        new_schedule: The new workout schedule
    """
    r = connect_to_redis()
    r.hset(f"my-workout-schedule:{user_id}", "workout_schedule", new_schedule)


# TODO: Refactor this file because I'm sure there is duplicated functionality
def get_cached_schedule_json(
    user_id: int,
    include_descriptions: bool = True,
    day_of_the_week: Optional[DaysOfTheWeek] = None,
):
    """
    Get the cached workout schedule for the user

    Args:
        user_id: The ID of the user
    """
    r = connect_to_redis()
    if not (
        cached_schedule := r.hget(f"my-workout-schedule:{user_id}", "workout_schedule")
    ):
        raise ValueError("No cached schedule found for this user.")

    cached_schedule_dict = json.loads(cached_schedule)

    if not day_of_the_week:
        return json.dumps(cached_schedule_dict, indent=2)
    cached_day_schedule = cached_schedule_dict[day_of_the_week]
    if not include_descriptions:
        for exercise in cached_day_schedule["exercises"]:
            exercise.pop("description")
    return json.dumps(cached_day_schedule, indent=2)


def edit_workout_schedule_json(
    agent_input: str,
    user_id: int,
    store_in_redis: bool = True,
) -> str:
    """
    Run the Edit JSON chain with the provided agent's input and the user's ID.

    Args:
        agent_input: The agent's input text for the conversation.
        user_id: The ID of the user.
        store_in_redis: Whether to store the updated schedule in Redis

    Returns:
        The updated workout schedule
    """
    new_schedule = init_edit_schedule_json_chain().predict(
        agent_input=agent_input,
        user_exercise_schedule_json=get_cached_schedule_json(user_id),
    )
    if store_in_redis:
        store_new_workout_schedule_json(user_id, new_schedule)

    return (
        "Your workout schedule has been updated! Here is your new schedule:\n\n"
        + new_schedule
    )


def edit_workout(
    agent_input: str,
    user_id: int,
    day_of_the_week: DaysOfTheWeek,
    store_in_redis: bool = True,
    edit_workout_description: bool = False,
) -> str:
    """
    Run the Edit JSON chain with the provided agent's input and the user's ID.

    Args:
        agent_input: The agent's input text for the conversation.
        user_id: The ID of the user.
        day_of_the_week: The day of the week to edit the workout for.
        store_in_redis: Whether to store the updated schedule in Redis
        edit_workout_description: Whether to edit the workout description

    Returns:
        The updated workout schedule
    """
    new_workout = init_edit_schedule_json_chain().predict(
        agent_input=agent_input,
        user_exercise_schedule_json=get_cached_schedule_json(
            user_id,
            include_descriptions=edit_workout_description,
            day_of_the_week=day_of_the_week,
        ),
    )
    if store_in_redis:
        store_new_workout(user_id, new_workout, day_of_the_week)

    return (
        "Your workout schedule has been updated! Here is your new schedule:\n\n"
        + new_workout
    )
