CREATE TABLE custom_daily_meal_plan_and_meal
(
    custom_daily_meal_plan_id integer NOT NULL
        REFERENCES custom_daily_meal_plan
            ON DELETE CASCADE,
    meal_id                   integer NOT NULL
        REFERENCES meal
            ON DELETE CASCADE,
    PRIMARY KEY (custom_daily_meal_plan_id, meal_id)
);

ALTER TABLE custom_daily_meal_plan_and_meal
    OWNER TO root;

INSERT INTO public.custom_daily_meal_plan_and_meal (custom_daily_meal_plan_id, meal_id) VALUES (1, 1);
INSERT INTO public.custom_daily_meal_plan_and_meal (custom_daily_meal_plan_id, meal_id) VALUES (1, 2);
INSERT INTO public.custom_daily_meal_plan_and_meal (custom_daily_meal_plan_id, meal_id) VALUES (1, 3);
INSERT INTO public.custom_daily_meal_plan_and_meal (custom_daily_meal_plan_id, meal_id) VALUES (1, 4);
INSERT INTO public.custom_daily_meal_plan_and_meal (custom_daily_meal_plan_id, meal_id) VALUES (1, 5);
