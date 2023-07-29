CREATE TABLE custom_weekly_meal_plan_and_custom_daily_meal_plan
(
    custom_weekly_meal_plan_id integer NOT NULL
        CONSTRAINT custom_weekly_meal_plan_and_cus_custom_weekly_meal_plan_id_fkey
            REFERENCES custom_weekly_meal_plan
            ON DELETE CASCADE,
    custom_daily_meal_plan_id  integer NOT NULL
        CONSTRAINT custom_weekly_meal_plan_and_cust_custom_daily_meal_plan_id_fkey
            REFERENCES custom_daily_meal_plan
            ON DELETE CASCADE,
    PRIMARY KEY (custom_daily_meal_plan_id, custom_weekly_meal_plan_id)
);

ALTER TABLE custom_weekly_meal_plan_and_custom_daily_meal_plan
    OWNER TO root;

