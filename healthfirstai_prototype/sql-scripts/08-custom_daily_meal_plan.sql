CREATE TABLE custom_daily_meal_plan
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    description text         NOT NULL
);

ALTER TABLE custom_daily_meal_plan
    OWNER TO root;

INSERT INTO public.custom_daily_meal_plan (id, name, description) VALUES (1, 'Default Daily Meal Plan', 'Default daily meal plan from bodybuilding.com');
