-- Fake data for country table
INSERT INTO country (name, continent)
VALUES ('United States', 'North America'),
       ('United Kingdom', 'Europe'),
       ('Canada', 'North America'),
       ('Germany', 'Europe'),
       ('Australia', 'Oceania');

-- Fake data for city table
INSERT INTO city (name, country_id)
VALUES ('New York', 1),
       ('London', 2),
       ('Toronto', 3),
       ('Berlin', 4),
       ('Sydney', 5);

-- Fake data for user table
-- FIXME: update the columns to match the actual table
INSERT INTO "user" (height, weight, gender, age, country_id, city_id)
VALUES (180.0, 75.0, 'Male', 30, 1, 1),
       (165.5, 60.8, 'Female', 28, 2, 2),
       (175.2, 80.0, 'Male', 35, 3, 3),
       (160.0, 55.0, 'Female', 25, 1, 2),
       (185.0, 90.5, 'Male', 40, 2, 3);

-- Fake data for workout table
INSERT INTO public.workout (workout_id, user_id, workout_name, workout_description)
VALUES (1, 1, 'Default Push Day', 'A comprehensive workout targeting chest, triceps, and shoulders.');
INSERT INTO public.workout (workout_id, user_id, workout_name, workout_description)
VALUES (2, 2, 'Default Pull Day', 'A comprehensive workout targeting biceps, back, and lats.');
INSERT INTO public.workout (workout_id, user_id, workout_name, workout_description)
VALUES (3, 3, 'Default Leg Day', 'A comprehensive workout targeting calves, hamstrings, and glutes');
INSERT INTO public.workout (workout_id, user_id, workout_name, workout_description)
VALUES (4, 4, 'Cardio', 'A cardio workout to raise your heartbeat and improve your cardiovascular system.');


-- Fake data for workout_exercise table
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (1, 1, 943, 3, 8, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (2, 1, 2546, 3, 16, 5, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (3, 1, 2535, 3, 10, 15, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (4, 1, 1060, 3, 12, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (5, 1, 1473, 3, 10, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (6, 2, 1507, 3, 8, 0, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (7, 2, 737, 3, 10, 5, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (8, 2, 2688, 2, 18, 15, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (9, 2, 1481, 2, 18, 15, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (10, 2, 770, 3, 13, 5, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (11, 3, 1800, 3, 8, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (12, 3, 888, 3, 12, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (13, 3, 1347, 3, 10, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (14, 3, 2075, 3, 10, 30, NULL);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (15, 4, 2078, 0, 0, 0, 20);
INSERT INTO public.workout_exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, weight, duration)
VALUES (16, 4, 2001, 0, 0, 0, 20);


-- Fake data for user_workout_schedule table
INSERT INTO user_workout_schedule (user_id, workout_id, schedule_day, schedule_time)
VALUES (1, 1, 'Monday', '09:00:00'),
       (1, 2, 'Wednesday', '15:30:00'),
       (1, 3, 'Friday', '07:45:00'),
       (2, 2, 'Tuesday', '18:00:00'),
       (2, 3, 'Thursday', '16:00:00'),
       (3, 1, 'Tuesday', '08:00:00'),
       (3, 4, 'Thursday', '17:00:00'),
       (5, 4, 'Wednesday', '13:00:00');

