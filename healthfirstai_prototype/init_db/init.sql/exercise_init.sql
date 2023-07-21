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
    Exercise_type_ID SERIAL PRIMARY KEY,
    Exercise_type TEXT NOT NULL
);

CREATE TABLE body_parts (
    BodyPart_ID SERIAL PRIMARY KEY,
    BodyPart_Name VARCHAR(50) NOT NULL
);

CREATE TABLE equipment (
    Equipment_ID SERIAL PRIMARY KEY,
    Equipment_Name VARCHAR(50) NOT NULL
);

CREATE TABLE difficulty (
    Difficulty_ID SERIAL PRIMARY KEY,
    Difficulty_Name VARCHAR(50) NOT NULL
);

CREATE TABLE exercise (
    Exercise_ID SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT NOT NULL,
    BodyPart_ID INT NOT NULL,
    Exercise_type_ID INT NOT NULL,
    Equipment_ID INT NOT NULL,
    Difficulty_ID INT,

    FOREIGN KEY (Exercise_type_ID) REFERENCES exercise_type (Exercise_type_ID) ON DELETE CASCADE,
    FOREIGN KEY (BodyPart_ID) REFERENCES body_parts (BodyPart_ID) ON DELETE CASCADE,
    FOREIGN KEY (Equipment_ID) REFERENCES equipment (Equipment_ID) ON DELETE CASCADE,
    FOREIGN KEY (Difficulty_ID) REFERENCES difficulty (Difficulty_ID) ON DELETE CASCADE
);

CREATE TABLE workout (
    Workout_ID SERIAL PRIMARY KEY,
    User_ID INT NOT NULL,
    Workout_Name TEXT NOT NULL,
    Workout_Description TEXT,
    FOREIGN KEY (User_ID) REFERENCES "user" (ID) ON DELETE CASCADE
);

CREATE TABLE workout_exercise (
    workout_exercise_ID SERIAL PRIMARY KEY,
    Workout_ID INT NOT NULL,
    Exercise_ID INT NOT NULL,
    Sets INT NOT NULL,
    Reps INT NOT NULL,
    Weight INT NOT NULL,
    Duration INT,
    FOREIGN KEY (Workout_ID) REFERENCES workout (Workout_ID) ON DELETE CASCADE,
    FOREIGN KEY (Exercise_ID) REFERENCES exercise (Exercise_ID) ON DELETE CASCADE
);

CREATE TABLE user_workout_schedule (
    Schedule_ID SERIAL PRIMARY KEY,
    User_ID INT NOT NULL,
    Workout_ID INT NOT NULL,
    Schedule_Day VARCHAR(10) NOT NULL,
    Schedule_Time TIME NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES "user" (ID) ON DELETE CASCADE,
    FOREIGN KEY (Workout_ID) REFERENCES workout (Workout_ID) ON DELETE CASCADE
);

