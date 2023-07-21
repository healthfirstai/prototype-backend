CREATE TABLE meal_ingredient
(
    meal_id             integer       NOT NULL
        REFERENCES meal
            ON DELETE CASCADE,
    ingredient_id       integer       NOT NULL
        REFERENCES food
            ON DELETE CASCADE,
    unit_of_measurement varchar(255)  NOT NULL
        REFERENCES unit_of_measurement
            ON DELETE CASCADE,
    quantity            numeric(5, 2) NOT NULL,
    PRIMARY KEY (meal_id, ingredient_id)
);

ALTER TABLE meal_ingredient
    OWNER TO root;

INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (1, 171304, 'cups', 1.50);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (1, 167755, 'cups', 0.50);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (1, 167542, 'cups', 0.33);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (1, 171287, 'units', 3.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 173177, 'scoops', 2.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 170173, 'cups', 0.25);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 171719, 'cups', 0.75);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 169414, 'tbsp', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 169593, 'tbsp', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 175103, 'cubes', 3.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (2, 173234, 'cups', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 169247, 'leaves', 2.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 174752, 'oz', 8.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 170457, 'slices', 2.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 170000, 'slices', 2.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 168556, 'tbsp', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 167736, 'tbsp', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (3, 169963, 'cups', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (4, 173158, 'bar', 1.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (5, 171971, 'oz', 6.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (5, 168875, 'cups', 0.25);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (5, 168462, 'cups', 4.00);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (5, 173420, 'cups', 0.25);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (5, 168550, 'units', 0.50);
INSERT INTO public.meal_ingredient (meal_id, ingredient_id, unit_of_measurement, quantity) VALUES (5, 171413, 'tbsp', 2.00);
