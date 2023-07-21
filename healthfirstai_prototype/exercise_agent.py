# NOTE: This is where the main application logic is implemented for the exercise agent
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_
from sqlalchemy.orm import sessionmaker, declarative_base
from langchain.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def generate_schedule_json(user_id):
    # change echo to see the SQL statements
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3307/healthfirstai', echo=False)
    Base = declarative_base()

    class ExerciseType(Base):
        __tablename__ = 'exercise_type'
        Exercise_type_ID = Column(Integer, primary_key=True)
        Exercise_type = Column(String, nullable=False)

    class BodyPart(Base):
        __tablename__ = 'body_parts'
        BodyPart_ID = Column(Integer, primary_key=True)
        BodyPart_Name = Column(String(50), nullable=False)

    class Exercise(Base):
        __tablename__ = 'exercise'
        Exercise_ID = Column(Integer, primary_key=True)
        Name = Column(String, nullable=False)
        Description = Column(String, nullable=False)
        Exercise_type_ID = Column(Integer, ForeignKey('exercise_type.Exercise_type_ID'), nullable=False)
        Equipment = Column(String, nullable=False)
        Difficulty = Column(String)

    class ExerciseBodyPart(Base):
        __tablename__ = 'exercise_body_part'
        Exercise_BodyPart_ID = Column(Integer, primary_key=True)
        BodyPart_ID = Column(Integer, ForeignKey('body_parts.BodyPart_ID'), nullable=False)
        Exercise_ID = Column(Integer, ForeignKey('exercise.Exercise_ID'), nullable=False)

    class Workout(Base):
        __tablename__ = 'workout'
        Workout_ID = Column(Integer, primary_key=True)
        User_ID = Column(Integer, nullable=False)
        Workout_Name = Column(String, nullable=False)
        Workout_Description = Column(String)

    class WorkoutExercise(Base):
        __tablename__ = 'workout_exercise'
        workout_exercise_ID = Column(Integer, primary_key=True)
        Workout_ID = Column(Integer, ForeignKey('workout.Workout_ID'), nullable=False)
        Exercise_ID = Column(Integer, ForeignKey('exercise.Exercise_ID'), nullable=False)
        Sets = Column(Integer, nullable=False)
        Reps = Column(Integer, nullable=False)
        Weight = Column(Integer, nullable=False)
        Duration = Column(Integer)

    class UserWorkoutSchedule(Base):
        __tablename__ = 'user_workout_schedule'
        Schedule_ID = Column(Integer, primary_key=True)
        User_ID = Column(Integer, nullable=False)
        Workout_ID = Column(Integer, ForeignKey('workout.Workout_ID'), nullable=False)
        Schedule_Day = Column(String(10), nullable=False)
        Schedule_Time = Column(String, nullable=False)

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
                .join(ExerciseBodyPart)
                .join(BodyPart)
                .all()
            )

            for workout_exercise in workout_exercises:
                exercise_id = workout_exercise.Exercise_ID
                exercise = session.query(Exercise).filter_by(Exercise_ID=exercise_id).first()
                exercise_type = session.query(ExerciseType.Exercise_type).filter_by(
                    Exercise_type_ID=exercise.Exercise_type_ID
                ).scalar()
                body_parts = (
                    session.query(BodyPart.BodyPart_Name)
                    .join(ExerciseBodyPart, and_(ExerciseBodyPart.BodyPart_ID == BodyPart.BodyPart_ID))
                    .filter(and_(ExerciseBodyPart.Exercise_ID == exercise_id))
                    .all()
                )

                exercise_info = {
                    'Exercise_ID': exercise_id,
                    'Name': exercise.Name,
                    'Description': exercise.Description,
                    'Exercise_Type': exercise_type,
                    'Equipment': exercise.Equipment,
                    'Difficulty': exercise.Difficulty,
                    'Body_Part': [bp.BodyPart_Name for bp in body_parts],
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

        print("Schedule JSON file generated successfully.")

    except Exception as e:
        print("Error occurred while generating schedule JSON file: ", e)

    finally:
        # Close the session when done
        session.close()


if __name__ == '__main__':
    # generate_schedule_json(1)
    OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
    llm = OpenAI(temperature=0, openai_api_key=OPEN_AI_API_KEY)
