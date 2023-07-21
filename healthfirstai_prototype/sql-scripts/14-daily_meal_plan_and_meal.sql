CREATE TABLE daily_meal_plan_and_meal
(
    base_daily_meal_plan_id integer NOT NULL
        REFERENCES base_daily_meal_plan
            ON DELETE CASCADE,
    meal_id                 integer NOT NULL
        REFERENCES meal
            ON DELETE CASCADE,
    PRIMARY KEY (base_daily_meal_plan_id, meal_id)
);

ALTER TABLE daily_meal_plan_and_meal
    OWNER TO root;

INSERT INTO public.daily_meal_plan_and_meal (base_daily_meal_plan_id, meal_id) VALUES (1, 1);
INSERT INTO public.daily_meal_plan_and_meal (base_daily_meal_plan_id, meal_id) VALUES (1, 2);
INSERT INTO public.daily_meal_plan_and_meal (base_daily_meal_plan_id, meal_id) VALUES (1, 3);
INSERT INTO public.daily_meal_plan_and_meal (base_daily_meal_plan_id, meal_id) VALUES (1, 4);
INSERT INTO public.daily_meal_plan_and_meal (base_daily_meal_plan_id, meal_id) VALUES (1, 5);
