-- Fake data for country table
INSERT INTO country (name, continent)
VALUES
    ('United States', 'North America'),
    ('United Kingdom', 'Europe'),
    ('Canada', 'North America'),
    ('Germany', 'Europe'),
    ('Australia', 'Oceania');

-- Fake data for city table
INSERT INTO city (name, country_id)
VALUES
    ('New York', 1),
    ('London', 2),
    ('Toronto', 3),
    ('Berlin', 4),
    ('Sydney', 5);

-- Fake data for user table
-- FIXME: update the columns to match the actual table
INSERT INTO "user" (height, weight, gender, age, country_id, city_id)
VALUES
    (180.0, 75.0, 'Male', 30, 1, 1),
    (165.5, 60.8, 'Female', 28, 2, 2),
    (175.2, 80.0, 'Male', 35, 3, 3),
    (160.0, 55.0, 'Female', 25, 1, 2),
    (185.0, 90.5, 'Male', 40, 2, 3);

-- Fake data for workout table
INSERT INTO workout (user_id, workout_name, workout_description)
VALUES
    (1, 'Full Body Workout', 'A comprehensive workout targeting all muscle groups'),
    (2, 'Leg Day', 'Focused on leg exercises'),
    (3, 'Cardio Blast', 'High-intensity cardio workout'),
    (4, 'Upper Body Strength', 'Strength training for the upper body'),
    (5, 'Core Strength', 'Exercises to strengthen the core');

-- Fake data for workout_exercise table
INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, weight, duration)
VALUES
    (1, 1, 3, 10, 30, NULL),
    (1, 2, 4, 12, 60, NULL),
    (2, 2, 5, 8, 80, NULL),
    (3, 3, 3, 4, 4, NULL),
    (4, 4, 3, 8, 69, NULL);

-- Fake data for user_workout_schedule table
INSERT INTO user_workout_schedule (user_id, workout_id, schedule_day, schedule_time)
VALUES
    (1, 1, 'Monday', '09:00:00'),
    (1, 2, 'Wednesday', '15:30:00'),
    (1, 3, 'Friday', '07:45:00'),
    (2, 2, 'Tuesday', '18:00:00'),
    (2, 3, 'Thursday', '16:00:00'),
    (3, 1, 'Tuesday', '08:00:00'),
    (3, 4, 'Thursday', '17:00:00'),
    (4, 5, 'Monday', '10:30:00'),
    (5, 4, 'Wednesday', '13:00:00'),
    (5, 5, 'Friday', '09:30:00');
