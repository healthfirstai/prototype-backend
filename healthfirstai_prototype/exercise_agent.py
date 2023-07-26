# NOTE: This is where the main application logic is implemented for the exercise agent
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_
from sqlalchemy.orm import sessionmaker, declarative_base
from langchain.llms.openai import OpenAI
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
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    Base = declarative_base()

    class ExerciseType(Base):
        __tablename__ = 'exercise_type'
        exercise_type_id = Column(Integer, primary_key=True)
        exercise_type = Column(String, nullable=False)

    class BodyPart(Base):
        __tablename__ = 'body_parts'
        bodypart_id = Column(Integer, primary_key=True)
        bodypart_name = Column(String(50), nullable=False)

    class Difficulty(Base):
        __tablename__ = 'difficulty'
        difficulty_id = Column(Integer, primary_key=True)
        difficulty_name = Column(String(50), nullable=False)

    class Equipment(Base):
        __tablename__ = 'equipment'
        equipment_id = Column(Integer, primary_key=True)
        equipment_name = Column(String(50), nullable=False)

    class Exercise(Base):
        __tablename__ = 'exercise'
        exercise_id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        description = Column(String, nullable=False)
        bodypart_id = Column(Integer, ForeignKey('body_parts.bodypart_id'), nullable=False)
        exercise_type_id = Column(Integer, ForeignKey('exercise_type.exercise_type_id'), nullable=False)
        equipment_id = Column(String, ForeignKey('equipment.equipment_name'), nullable=False)
        difficulty_id = Column(String, ForeignKey('difficulty.difficulty_name'), nullable=False)

    class Workout(Base):
        __tablename__ = 'workout'
        workout_id = Column(Integer, primary_key=True)
        user_id = Column(Integer, nullable=False)
        workout_name = Column(String, nullable=False)
        workout_description = Column(String)

    class WorkoutExercise(Base):
        __tablename__ = 'workout_exercise'
        workout_exercise_id = Column(Integer, primary_key=True)
        workout_id = Column(Integer, ForeignKey('workout.workout_id'), nullable=False)
        exercise_id = Column(Integer, ForeignKey('exercise.exercise_id'), nullable=False)
        sets = Column(Integer, nullable=False)
        reps = Column(Integer, nullable=False)
        weight = Column(Integer, nullable=False)
        duration = Column(Integer)

    class UserWorkoutSchedule(Base):
        __tablename__ = 'user_workout_schedule'
        schedule_id = Column(Integer, primary_key=True)
        user_id = Column(Integer, nullable=False)
        workout_id = Column(Integer, ForeignKey('workout.workout_id'), nullable=False)
        schedule_day = Column(String(10), nullable=False)
        schedule_time = Column(String, nullable=False)

    Base.metadata.create_all(engine)
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

    except Exception as e:
        print("Error occurred while generating schedule JSON file: ", e)

    finally:
        # Close the session when done
        session.close()


if __name__ == '__main__':
    generate_schedule_json(1)
    OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
    llm = OpenAI(temperature=0, openai_api_key=OPEN_AI_API_KEY)
