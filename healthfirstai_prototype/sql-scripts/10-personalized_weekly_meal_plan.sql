CREATE TABLE personalized_weekly_meal_plan
(
    id                      serial
        PRIMARY KEY,
    user_id                 integer NOT NULL
        REFERENCES "user"
            ON DELETE CASCADE,
    custom_weekly_meal_plan integer NOT NULL
        REFERENCES custom_weekly_meal_plan
            ON DELETE CASCADE,
    start_date              date    NOT NULL,
    end_date                date    NOT NULL,
    goal_id                 integer NOT NULL
        REFERENCES goals
            ON DELETE CASCADE
);

ALTER TABLE personalized_weekly_meal_plan
    OWNER TO root;

