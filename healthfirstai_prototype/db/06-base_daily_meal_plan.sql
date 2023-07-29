CREATE TABLE base_daily_meal_plan
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    description text         NOT NULL,
    link        varchar(255)
);

ALTER TABLE base_daily_meal_plan
    OWNER TO root;

INSERT INTO public.base_daily_meal_plan (id, name, description, link) VALUES (1, 'Default Daily Meal Plan', 'Default daily meal plan from bodybuilding.com', 'https://www.bodybuilding.com/content/meal-plan-for-every-guy.html');
