from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

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
