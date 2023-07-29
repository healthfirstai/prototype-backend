CREATE TABLE meal
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    meal_type   varchar(10)  NOT NULL
        CONSTRAINT meal_meal_type_check
            CHECK ((meal_type)::text = ANY
                   (ARRAY [('Breakfast'::character varying)::text, ('Lunch'::character varying)::text, ('Dinner'::character varying)::text, ('Snack'::character varying)::text, ('Drink'::character varying)::text, ('Other'::character varying)::text])),
    description text
);

ALTER TABLE meal
    OWNER TO root;

INSERT INTO public.meal (id, name, meal_type, description) VALUES (5, 'Default Dinner', 'Dinner', 'Shrimp With Spinach Salad & Brown Rice');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (1, 'Default Breakfast', 'Breakfast', 'Greek Yogurt & Fruit breakfast');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (4, 'Default Snack', 'Snack', 'Post-Workout Nutrition');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (3, 'Default Lunch', 'Lunch', 'Bibb Lettuce Burger');
INSERT INTO public.meal (id, name, meal_type, description) VALUES (2, 'Default Drink', 'Drink', 'Double Chocolate Cherry Smoothie');
