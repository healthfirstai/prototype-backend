import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from exercise_data_models import (
    ExerciseType,
    BodyPart,
    Difficulty,
    Equipment,
    Exercise,
    UserWorkoutSchedule,
    Workout,
    WorkoutExercise,
)
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER") or ""
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or ""
DB_HOST = os.getenv("POSTGRES_HOST") or ""
DB_NAME = os.getenv("POSTGRES_DATABASE") or ""
DB_PORT = os.getenv("POSTGRES_PORT") or ""


def generate_schedule_json(user_id):
    # change echo to see the SQL statements
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
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

            for workout_exercise in workout_exercises:
                exercise_id = workout_exercise.exercise_id
                exercise = session.query(Exercise).filter_by(exercise_id=exercise_id).first()
                exercise_type = session.query(ExerciseType.exercise_type).filter_by(
                    exercise_type_id=exercise.exercise_type_id
                ).scalar()
                body_parts = session.query(BodyPart.bodypart_name).filter_by(
                    bodypart_id=exercise.bodypart_id
                ).scalar()
                difficulty = session.query(Difficulty.difficulty_name).filter_by(
                    difficulty_id=exercise.difficulty_id
                ).scalar()
                equipment = session.query(Equipment.equipment_name).filter_by(
                    equipment_id=exercise.equipment_id
                ).scalar()

                exercise_info = {
                    'exercise_id': exercise_id,
                    'name': exercise.name,
                    'description': exercise.description,
                    'exercise_type': exercise_type,
                    'equipment': equipment,
                    'difficulty': difficulty,
                    'body_part': body_parts,
                    'reps': workout_exercise.reps,
                    'sets': workout_exercise.sets
                }
                exercise_dict[exercise_id] = exercise_info

                schedule_info = {
                    'schedule_day': schedule_day,
                    'schedule_time': str(schedule_time),
                    'workout_name': workout.workout_name,
                    'workout_description': workout.workout_description,
                    'exercises': list(exercise_dict.values())
                }

                schedule_json[schedule_id] = schedule_info

                # Write the JSON data to a file
        with open('user_schedule.json', 'w') as json_file:
            json.dump(schedule_json, json_file, indent=4)

        print("Schedule JSON file generated successfully!")

    except Exception as e:
        print("Error occurred while generating schedule JSON file: ", e)

    finally:
        # Close the session when done
        session.close()


if __name__ == '__main__':
    generate_schedule_json(1)
