# NOTE: This is where the main application logic is implemented for the exercise agent
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

def generate_schedule_json(user_id):
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3307/healthfirstai', echo=True)
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        schedules = relationship("UserWorkoutSchedule", back_populates="user")

    class Workout(Base):
        __tablename__ = 'workout'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        description = Column(String)
        exercises = relationship("WorkoutExercise", back_populates="workout")

    class Exercise(Base):
        __tablename__ = 'exercise'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        description = Column(String)
        exercise_type = Column(String)
        equipment = Column(String)
        difficulty = Column(String)
        body_parts = relationship("BodyPart", secondary='exercise_body_part')

    class UserWorkoutSchedule(Base):
        __tablename__ = 'user_workout_schedule'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'))
        schedule_day = Column(String)
        schedule_time = Column(String)
        workout_id = Column(Integer, ForeignKey('workout.id'))
        user = relationship("User", back_populates="schedules")
        workout = relationship("Workout")

    class WorkoutExercise(Base):
        __tablename__ = 'workout_exercise'
        id = Column(Integer, primary_key=True)
        workout_id = Column(Integer, ForeignKey('workout.id'))
        exercise_id = Column(Integer, ForeignKey('exercise.id'))
        reps = Column(Integer)
        sets = Column(Integer)
        workout = relationship("Workout", back_populates="exercises")
        exercise = relationship("Exercise")

    class ExerciseBodyPart(Base):
        __tablename__ = 'exercise_body_part'
        id = Column(Integer, primary_key=True)
        exercise_id = Column(Integer, ForeignKey('exercise.id'))
        body_part_id = Column(Integer, ForeignKey('body_parts.id'))

    class BodyPart(Base):
        __tablename__ = 'body_parts'
        id = Column(Integer, primary_key=True)
        name = Column(String)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        # Query to fetch the user's schedule along with workout details
        user_schedules = session.query(UserWorkoutSchedule).filter_by(user_id=user_id).all()

        # Initialize the schedule dictionary
        schedule_json = {}

        for user_schedule in user_schedules:
            schedule_id = user_schedule.id
            schedule_day = user_schedule.schedule_day
            schedule_time = user_schedule.schedule_time
            workout_id = user_schedule.workout_id
            workout_name = user_schedule.workout.name
            workout_desc = user_schedule.workout.description

            exercise_dict = {}
            for exercise in user_schedule.workout.exercises:
                exercise_id = exercise.exercise_id
                exercise_name = exercise.exercise.name
                exercise_desc = exercise.exercise.description
                exercise_type = exercise.exercise.exercise_type
                exercise_equipment = exercise.exercise.equipment
                exercise_difficulty = exercise.exercise.difficulty
                body_part_names = [bp.name for bp in exercise.exercise.body_parts]
                reps = exercise.reps
                sets = exercise.sets

                exercise_info = {
                    'Exercise_ID': exercise_id,
                    'Name': exercise_name,
                    'Description': exercise_desc,
                    'Exercise_Type': exercise_type,
                    'Equipment': exercise_equipment,
                    'Difficulty': exercise_difficulty,
                    'Body_Part': body_part_names,
                    'Reps': reps,
                    'Sets': sets
                }
                exercise_dict[exercise_id] = exercise_info

            schedule_info = {
                'Schedule_Day': schedule_day,
                'Schedule_Time': str(schedule_time),
                'Workout_ID': workout_id,
                'Workout_Name': workout_name,
                'Workout_Description': workout_desc,
                'Exercises': list(exercise_dict.values())
            }

            schedule_json[schedule_id] = schedule_info

        # Write the JSON data to a file
        with open('user_schedule.json', 'w') as json_file:
            json.dump(schedule_json, json_file, indent=4)

        print("Schedule JSON file generated successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the session when done
        session.close()

if __name__ == '__main__':
    generate_schedule_json(1)

