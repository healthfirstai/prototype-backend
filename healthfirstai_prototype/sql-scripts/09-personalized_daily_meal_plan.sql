CREATE TABLE personalized_daily_meal_plan
(
    id                     serial
        PRIMARY KEY,
    user_id                integer NOT NULL
        REFERENCES "user"
            ON DELETE CASCADE,
    custom_daily_meal_plan integer NOT NULL
        REFERENCES custom_daily_meal_plan
            ON DELETE CASCADE,
    start_date             date    NOT NULL,
    end_date               date    NOT NULL,
    goal_id                integer NOT NULL
        REFERENCES goals
            ON DELETE CASCADE
);

ALTER TABLE personalized_daily_meal_plan
    OWNER TO root;

INSERT INTO public.personalized_daily_meal_plan (id, user_id, custom_daily_meal_plan, start_date, end_date, goal_id) VALUES (1, 1, 1, '2020-01-01', '2021-02-01', 1);
