-- REMOVE DATA FROM ALL TABLES
DELETE FROM `user_workout_schedule`;
DELETE FROM `workout_exercise`;
DELETE FROM `workout`;
DELETE FROM `exercise`;
DELETE FROM exercise_type;
DELETE FROM body_parts;
DELETE FROM `user`;
DELETE FROM `city`;
DELETE FROM `country`;


-- Fake data for `country` table
INSERT INTO `country` (id, `name`, `continent`)
VALUES
    (1, 'United States', 'North America'),
    (2, 'United Kingdom', 'Europe'),
    (3, 'Canada', 'North America'),
    (4, 'Germany', 'Europe'),
    (5, 'Australia', 'Oceania');

-- Fake data for `city` table
INSERT INTO `city` (id, `name`, `country_id`)
VALUES
    (1, 'New York', 1),
    (2, 'London', 2),
    (3, 'Toronto', 3),
    (4, 'Berlin', 4),
    (5, 'Sydney', 5);

-- Fake data for `user` table
INSERT INTO `user` (id, `username`, `height`, `weight`, `gender`, `age`, `country_id`, `city_id`)
VALUES
    (1,'JohnDoe', 180.0, 75.0, 'Male', 30, 1, 1),
    (2, 'JaneSmith', 165.5, 60.8, 'Female', 28, 2, 2),
    (3, 'MarkJohnson', 175.2, 80.0, 'Male', 35, 3, 3),
    (4, 'EmilyBrown', 160.0, 55.0, 'Female', 25, 1, 2),
    (5, 'MichaelLee', 185.0, 90.5, 'Male', 40, 2, 3);

-- Real data for `exercise_type` table
INSERT INTO `exercise_type` (`Exercise_Type_ID`, `Exercise_type`)
VALUES
    (1, 'Strength'),
    (2, 'Cardio'),
    (3, 'Flexibility');

-- Real data for `body_parts` table
INSERT INTO body_parts (bodypart_id, BodyPart_Name) VALUES
    (1, 'Quadriceps'),
    (2, 'Hamstrings'),
    (3, 'Glutes'),
    (4, 'Calves'),
    (5, 'Front Abs (Rectus Abdominis)'),
    (6, 'Obliques'),
    (7, 'Lats (Latissimus Dorsi)'),
    (8, 'Upper back and Neck (Trapezius)'),
    (9, 'Lower back (Erector Spinae)'),
    (10, 'Chest (Pectoralis Major)'),
    (11, 'Deltoids'),
    (12, 'Biceps'),
    (13, 'Triceps'),
    (14, 'Forearms'),
    (15, 'Heart & Lungs');

-- Fake data for `exercise` table
INSERT INTO `exercise` (`Exercise_ID`, `Name`, `Description`, Exercise_type_ID, `Equipment`, `Difficulty`)
VALUES
    (1, 'Push-ups', 'Classic upper body exercise', 1, 'Bodyweight', 'Beginner'),
    (2, 'Squats', 'Lower body exercise', 1, 'Barbell', 'Intermediate'),
    (3, 'Running', 'Cardiovascular exercise', 2, 'None', 'Intermediate'),
    (4, 'Pull-ups', 'Upper body exercise', 1, 'Pull-up bar', 'Intermediate'),
    (5, 'Plank', 'Core exercise', 1, 'None', 'Beginner'),
    (6, 'Bench Press', 'Upper body exercise', 1, 'Barbell', 'Intermediate'),
    (7, 'Deadlift', 'Total body exercise', 1, 'Barbell', 'Advanced'),
    (8, 'Cycling', 'Cardiovascular exercise', 2, 'Stationary bike', 'Intermediate'),
    (9, 'Bicep Curls', 'Upper body exercise', 1, 'Dumbbells', 'Beginner'),
    (10, 'Yoga', 'Mind-body exercise', 3, 'Yoga mat', 'Beginner');

-- Fake data for `exercise_body_part` table
INSERT INTO exercise_body_part (BodyPart_ID, Exercise_ID) VALUES
    (10, 1), -- Push-ups target Chest (Pectoralis Major)
    (11, 1), -- Push-ups target Deltoids
    (1, 2), -- Squats target Quadriceps
    (2, 2), -- Squats target Hamstrings
    (3, 2), -- Squats target Glutes
    (4, 2), -- Squats target Calves
    (5, 5), -- Plank targets Front Abs (Rectus Abdominis)
    (6, 5), -- Plank targets Obliques
    (10, 6), -- Bench Press targets Chest (Pectoralis Major)
    (11, 6), -- Bench Press targets Deltoids
    (1, 7), -- Deadlift targets Quadriceps
    (2, 7), -- Deadlift targets Hamstrings
    (9, 9), -- Bicep Curls target Biceps
    (13, 9), -- Bicep Curls target Triceps
    (15, 3); -- Running targets Heart & Lungs

-- Fake data for `workout` table
INSERT INTO `workout` (`Workout_ID`, `User_ID`, `Workout_Name`, `Workout_Description`)
VALUES
    (1, 1, 'Full Body Workout', 'A comprehensive workout targeting all muscle groups'),
    (2, 2, 'Leg Day', 'Focused on leg exercises'),
    (3, 3, 'Cardio Blast', 'High-intensity cardio workout'),
    (4, 4, 'Upper Body Strength', 'Strength training for the upper body'),
    (5, 5, 'Core Strength', 'Exercises to strengthen the core');

-- Fake data for `workout_exercise` table
INSERT INTO `workout_exercise` (`workout_exercise_ID`, `Workout_ID`, `Exercise_ID`, `Sets`, `Reps`, `Weight`)
VALUES
    (1, 1, 1, 3, 10, 30),
    (2, 1, 2, 4, 12, 60),
    (3, 2, 2, 5, 8, 80),
    (4, 3, 3, 3, 4, 4),
    (5, 4, 4, 3, 8, 69);

INSERT INTO `user_workout_schedule` (`User_ID`, `Workout_ID`, `Schedule_Day`, `Schedule_Time`)
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