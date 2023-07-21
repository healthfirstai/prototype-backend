CREATE TABLE meal
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    meal_type   varchar(10)  NOT NULL
        CONSTRAINT meal_meal_type_check
            CHECK ((meal_type)::text = ANY
                   ((ARRAY ['Breakfast'::character varying, 'Lunch'::character varying, 'Dinner'::character varying, 'Snack'::character varying, 'Drink'::character varying, 'Other'::character varying])::text[])),
    description text
);

ALTER TABLE meal
    OWNER TO root;

INSERT INTO public.meal (id, name, meal_type, description) VALUES (1, 'Default Meal 1', 'Breakfast', 'Greek Yogurt & Fruit breakfast');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (2, 'Default Meal 2', 'Drink', 'Double Chocolate Cherry Smoothie');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (3, 'Default Meal 3', 'Lunch', 'Bibb Lettuce Burger');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (4, 'Default Meal 4', 'Snack', 'Post-Workout Nutrition');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (5, 'Default Meal 5', 'Dinner', 'Shrimp With Spinach Salad & Brown Rice');
