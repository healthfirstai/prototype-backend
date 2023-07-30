DROP TABLE IF EXISTS user_workout_schedule;
DROP TABLE IF EXISTS workout_exercise;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS exercise_type;
DROP TABLE IF EXISTS difficulty;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS workout;
DROP TABLE IF EXISTS body_parts;

CREATE TABLE exercise_type (
    exercise_type_id SERIAL PRIMARY KEY,
    exercise_type TEXT NOT NULL
);

CREATE TABLE body_parts (
    bodyPart_id SERIAL PRIMARY KEY,
    bodyPart_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(50) NOT NULL
);

CREATE TABLE difficulty (
    difficulty_id SERIAL PRIMARY KEY,
    difficulty_name VARCHAR(50) NOT NULL
);

CREATE TABLE exercise (
    exercise_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    bodypart_id INT NOT NULL,
    exercise_type_id INT NOT NULL,
    equipment_id INT NOT NULL,
    difficulty_id INT,

    FOREIGN KEY (exercise_type_id) REFERENCES exercise_type (exercise_type_id) ON DELETE CASCADE,
    FOREIGN KEY (bodypart_id) REFERENCES body_parts (bodypart_id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment (equipment_id) ON DELETE CASCADE,
    FOREIGN KEY (difficulty_id) REFERENCES difficulty (difficulty_id) ON DELETE CASCADE
);

CREATE TABLE workout (
    workout_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    workout_name TEXT NOT NULL,
    workout_description TEXT,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE TABLE workout_exercise (
    workout_exercise_id SERIAL PRIMARY KEY,
    workout_id INT NOT NULL,
    exercise_id INT NOT NULL,
    sets INT NOT NULL,
    reps INT NOT NULL,
    weight INT NOT NULL,
    duration INT,
    FOREIGN KEY (workout_id) REFERENCES workout (workout_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercise (exercise_id) ON DELETE CASCADE
);

CREATE TABLE user_workout_schedule (
    schedule_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    workout_id INT NOT NULL,
    schedule_day VARCHAR(10) NOT NULL,
    schedule_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY (workout_id) REFERENCES workout (workout_id) ON DELETE CASCADE
);

