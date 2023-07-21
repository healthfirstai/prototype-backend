\c healthfirstai;

DROP TABLE IF EXISTS user_workout_schedule;
DROP TABLE IF EXISTS workout_exercise;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS exercise_type;
DROP TABLE IF EXISTS difficulty;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS workout;
DROP TABLE IF EXISTS body_parts;
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS country;

CREATE TABLE country
(
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    continent VARCHAR(255) NOT NULL
);

CREATE TABLE city
(
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES country (ID) ON DELETE CASCADE
);

CREATE TABLE "user"
(
    ID SERIAL PRIMARY KEY,
    height NUMERIC(5, 2) NOT NULL,
    weight NUMERIC(5, 2) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    age INT NOT NULL,
    country_id INT NOT NULL,
    city_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES country (ID) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES city (ID) ON DELETE CASCADE
);

CREATE TABLE exercise_type (
    exercise_type_ID SERIAL PRIMARY KEY,
    exercise_type TEXT NOT NULL
);

CREATE TABLE body_parts (
    bodyPart_ID SERIAL PRIMARY KEY,
    bodyPart_Name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE equipment (
    equipment_ID SERIAL PRIMARY KEY,
    equipment_Name VARCHAR(50) NOT NULL
);

CREATE TABLE difficulty (
    difficulty_ID SERIAL PRIMARY KEY,
    difficulty_Name VARCHAR(50) NOT NULL
);

CREATE TABLE exercise (
    exercise_ID SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    bodyPart_ID INT NOT NULL,
    exercise_type_ID INT NOT NULL,
    equipment_ID INT NOT NULL,
    difficulty_ID INT,

    FOREIGN KEY (exercise_type_ID) REFERENCES exercise_type (exercise_type_ID) ON DELETE CASCADE,
    FOREIGN KEY (bodyPart_ID) REFERENCES body_parts (bodyPart_ID) ON DELETE CASCADE,
    FOREIGN KEY (equipment_ID) REFERENCES equipment (equipment_ID) ON DELETE CASCADE,
    FOREIGN KEY (difficulty_ID) REFERENCES difficulty (difficulty_ID) ON DELETE CASCADE
);

CREATE TABLE workout (
    workout_ID SERIAL PRIMARY KEY,
    user_ID INT NOT NULL,
    workout_Name TEXT NOT NULL,
    workout_Description TEXT,
    FOREIGN KEY (user_ID) REFERENCES "user" (ID) ON DELETE CASCADE
);

CREATE TABLE workout_exercise (
    workout_exercise_ID SERIAL PRIMARY KEY,
    workout_ID INT NOT NULL,
    exercise_ID INT NOT NULL,
    sets INT NOT NULL,
    reps INT NOT NULL,
    weight INT NOT NULL,
    duration INT,
    FOREIGN KEY (workout_ID) REFERENCES workout (workout_ID) ON DELETE CASCADE,
    FOREIGN KEY (exercise_ID) REFERENCES exercise (exercise_ID) ON DELETE CASCADE
);

CREATE TABLE user_workout_schedule (
    schedule_ID SERIAL PRIMARY KEY,
    user_ID INT NOT NULL,
    workout_ID INT NOT NULL,
    schedule_Day VARCHAR(10) NOT NULL,
    schedule_Time TIME NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES "user" (ID) ON DELETE CASCADE,
    FOREIGN KEY (workout_ID) REFERENCES workout (workout_ID) ON DELETE CASCADE
);

