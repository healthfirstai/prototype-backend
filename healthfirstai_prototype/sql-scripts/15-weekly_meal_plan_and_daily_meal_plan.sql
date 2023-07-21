CREATE TABLE weekly_meal_plan_and_daily_meal_plan
(
    base_weekly_meal_plan_id integer NOT NULL
        CONSTRAINT weekly_meal_plan_and_daily_meal_p_base_weekly_meal_plan_id_fkey
            REFERENCES base_weekly_meal_plan
            ON DELETE CASCADE,
    base_daily_meal_plan_id  integer NOT NULL
        CONSTRAINT weekly_meal_plan_and_daily_meal_pl_base_daily_meal_plan_id_fkey
            REFERENCES base_daily_meal_plan
            ON DELETE CASCADE,
    PRIMARY KEY (base_daily_meal_plan_id, base_weekly_meal_plan_id)
);

ALTER TABLE weekly_meal_plan_and_daily_meal_plan
    OWNER TO root;

