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


# TODO: Fix this
def generate_schedule_json(user_id):
    # change echo to see the SQL statements
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    Base = declarative_base()

    class ExerciseType(Base):
        __tablename__ = 'exercise_type'
        exercise_type_ID = Column(Integer, primary_key=True)
        exercise_type = Column(String, nullable=False)

    class BodyPart(Base):
        __tablename__ = 'body_parts'
        bodyPart_ID = Column(Integer, primary_key=True)
        bodyPart_Name = Column(String(50), nullable=False)

    class Difficulty(Base):
        __tablename__ = 'difficulty'
        difficulty_ID = Column(Integer, primary_key=True)
        difficulty_Name = Column(String(50), nullable=False)

    class Equipment(Base):
        __tablename__ = 'equipment'
        equipment_ID = Column(Integer, primary_key=True)
        equipment_Name = Column(String(50), nullable=False)

    class Exercise(Base):
        __tablename__ = 'exercise'
        exercise_ID = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        description = Column(String, nullable=False)
        bodyPart_ID = Column(Integer, ForeignKey('body_parts.BodyPart_ID'), nullable=False)
        exercise_type_ID = Column(Integer, ForeignKey('exercise_type.Exercise_type_ID'), nullable=False)
        equipment_ID = Column(String, ForeignKey('equipment.Equipment_Name'), nullable=False)
        difficulty_ID = Column(String, ForeignKey('difficulty.Difficulty_Name'), nullable=False)

    class Workout(Base):
        __tablename__ = 'workout'
        workout_ID = Column(Integer, primary_key=True)
        user_ID = Column(Integer, nullable=False)
        workout_Name = Column(String, nullable=False)
        workout_Description = Column(String)

    class WorkoutExercise(Base):
        __tablename__ = 'workout_exercise'
        workout_exercise_ID = Column(Integer, primary_key=True)
        workout_ID = Column(Integer, ForeignKey('workout.Workout_ID'), nullable=False)
        exercise_ID = Column(Integer, ForeignKey('exercise.Exercise_ID'), nullable=False)
        sets = Column(Integer, nullable=False)
        reps = Column(Integer, nullable=False)
        weight = Column(Integer, nullable=False)
        duration = Column(Integer)

    class UserWorkoutSchedule(Base):
        __tablename__ = 'user_workout_schedule'
        schedule_ID = Column(Integer, primary_key=True)
        user_ID = Column(Integer, nullable=False)
        workout_ID = Column(Integer, ForeignKey('workout.Workout_ID'), nullable=False)
        schedule_Day = Column(String(10), nullable=False)
        schedule_Time = Column(String, nullable=False)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query to fetch the user's schedule along with workout details
        user_schedules = session.query(UserWorkoutSchedule).filter_by(User_ID=user_id).all()

        # Initialize the schedule dictionary
        schedule_json = {}

        for user_schedule in user_schedules:
            schedule_id = user_schedule.Schedule_ID
            schedule_day = user_schedule.Schedule_Day
            schedule_time = user_schedule.Schedule_Time
            workout_id = user_schedule.Workout_ID
            workout = session.query(Workout).filter_by(Workout_ID=workout_id).first()

            exercise_dict = {}
            workout_exercises = (
                session.query(WorkoutExercise)
                .filter_by(Workout_ID=workout_id)
                .join(Exercise)
                .join(ExerciseType)
                .join(Difficulty)
                .join(BodyPart)
                .all()
            )

            for workout_exercise in workout_exercises:
                exercise_id = workout_exercise.Exercise_ID
                exercise = session.query(Exercise).filter_by(Exercise_ID=exercise_id).first()
                exercise_type = session.query(ExerciseType.Exercise_type).filter_by(
                    Exercise_type_ID=exercise.Exercise_type_ID
                ).scalar()
                body_parts = session.query(BodyPart.BodyPart_Name).filter_by(
                    BodyPart_ID=exercise.BodyPart_ID
                ).scalar()
                difficulty = session.query(Difficulty.Difficulty_Name).filter_by(
                    Difficulty_ID=exercise.Difficulty_ID
                ).scalar()
                equipment = session.query(Equipment.Equipment_name).filter_by(
                    Equipment_ID=exercise.Equipment_ID
                ).scalar()

                exercise_info = {
                    'Exercise_ID': exercise_id,
                    'Name': exercise.Name,
                    'Description': exercise.Description,
                    'Exercise_Type': exercise_type,
                    'Equipment': equipment,
                    'Difficulty': difficulty,
                    'Body_Part': body_parts,
                    'Reps': workout_exercise.Reps,
                    'Sets': workout_exercise.Sets
                }
                exercise_dict[exercise_id] = exercise_info

                schedule_info = {
                    'Schedule_Day': schedule_day,
                    'Schedule_Time': str(schedule_time),
                    'Workout_Name': workout.Workout_Name,
                    'Workout_Description': workout.Workout_Description,
                    'Exercises': list(exercise_dict.values())
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
    # OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
    # llm = OpenAI(temperature=0, openai_api_key=OPEN_AI_API_KEY)
