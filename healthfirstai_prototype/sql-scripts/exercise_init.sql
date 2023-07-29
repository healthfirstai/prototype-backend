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
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    continent VARCHAR(255) NOT NULL
);

CREATE TABLE city
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES country (ID) ON DELETE CASCADE
);

CREATE TABLE "user"
(
    id         serial PRIMARY KEY,
    height     numeric(5, 2) NOT NULL,
    weight     numeric(5, 2) NOT NULL,
    gender     varchar(10)   NOT NULL
        CONSTRAINT user_gender_check
            CHECK ((gender)::text = ANY
                   (ARRAY [('Male'::character varying)::text, ('Female'::character varying)::text, ('Other'::character varying)::text])),
    country_id integer       NOT NULL,
    city_id    integer       NOT NULL,
    first_name varchar(50),
    last_name  varchar(50),
    username   varchar(50),
    password   varchar(100),
    dob        date

    FOREIGN KEY (country_id) REFERENCES country (id) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES city (id) ON DELETE CASCADE
);

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

