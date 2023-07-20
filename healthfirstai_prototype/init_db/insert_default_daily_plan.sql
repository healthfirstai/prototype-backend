INSERT INTO base_daily_meal_plan (name, description)
VALUES ('Default Daily Meal Plan',
        'Default daily meal plan from bodybuilding.com: https://www.bodybuilding.com/content/meal-plan-for-every-guy.html');

INSERT INTO meal (name, meal_type, description)
VALUES ('Default Meal 1', 'Breakfast', 'Greek Yogurt & Fruit breakfast'),
       ('Default Meal 2', 'Drink', 'Double Chocolate Cherry Smoothie'),
       ('Default Meal 3', 'Lunch', 'Bibb Lettuce Burger'),
       ('Default Meal 4', 'Snack', 'Post-Workout Nutrition'),
       ('Default Meal 5', 'Dinner', 'Shrimp With Spinach Salad & Brown Rice');


SELECT id
INTO mealId1
FROM meal
WHERE name = 'Default Meal 1';

SELECT id
INTO mealId2
FROM meal
WHERE name = 'Default Meal 2';

SELECT id
INTO mealId3
FROM meal
WHERE name = 'Default Meal 3';

SELECT id
INTO mealId4
FROM meal
WHERE name = 'Default Meal 4';

SELECT id
INTO mealId5
FROM meal
WHERE name = 'Default Meal 5';

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
VALUES ((SELECT id FROM mealId1), 173177, (SELECT ID FROM measurement WHERE unit = 'scoops'), 2),  -- Protein Powder
       ((SELECT id FROM mealId1), 170173, (SELECT ID FROM measurement WHERE unit = 'cups'), 0.25), -- Coconut Milk
       ((SELECT id FROM mealId1), 171719, (SELECT ID FROM measurement WHERE unit = 'cups'), 0.75), -- Cherries
       ((SELECT id FROM mealId1), 169414, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 1),    -- Flaxseeds
       ((SELECT id FROM mealId1), 169593, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 1),    -- Cocoa Powder
       ((SELECT id FROM mealId1), 175103, (SELECT ID FROM measurement WHERE unit = 'cubes'), 3),   -- Ice
       ((SELECT id FROM mealId1), 173234, (SELECT ID FROM measurement WHERE unit = 'cups'), 1); -- Water


INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
SELECT @mealId2, 173177, (SELECT id FROM measurement WHERE unit = 'scoops'), 2
UNION ALL
SELECT @mealId2, 170173, (SELECT id FROM measurement WHERE unit = 'cups'), 0.25
UNION ALL
SELECT @mealId2, 171719, (SELECT id FROM measurement WHERE unit = 'cups'), 0.75
UNION ALL
SELECT @mealId2, 169414, (SELECT id FROM measurement WHERE unit = 'tbsp'), 1
UNION ALL
SELECT @mealId2, 169593, (SELECT id FROM measurement WHERE unit = 'tbsp'), 1
UNION ALL
SELECT @mealId2, 175103, (SELECT id FROM measurement WHERE unit = 'cubes'), 3
UNION ALL
SELECT @mealId2, 173234, (SELECT id FROM measurement WHERE unit = 'cups'), 1;

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
SELECT @mealId3, 169247, (SELECT id FROM measurement WHERE unit = 'leaves'), 2
UNION ALL
SELECT @mealId3, 174752, (SELECT id FROM measurement WHERE unit = 'oz'), 8
UNION ALL
SELECT @mealId3, 170457, (SELECT id FROM measurement WHERE unit = 'slices'), 2
UNION ALL
SELECT @mealId3, 170000, (SELECT id FROM measurement WHERE unit = 'slices'), 2
UNION ALL
SELECT @mealId3, 168556, (SELECT id FROM measurement WHERE unit = 'tbsp'), 1
UNION ALL
SELECT @mealId3, 167736, (SELECT id FROM measurement WHERE unit = 'tbsp'), 1
UNION ALL
SELECT @mealId3, 169963, (SELECT id FROM measurement WHERE unit = 'cups'), 1;

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
SELECT @mealId4, 173158, (SELECT id FROM measurement WHERE unit = 'bar'), 1;

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
SELECT @mealId5, 171971, (SELECT id FROM measurement WHERE unit = 'oz'), 6
UNION ALL
SELECT @mealId5, 168875, (SELECT id FROM measurement WHERE unit = 'cups'), 0.25
UNION ALL
SELECT @mealId5, 168462, (SELECT id FROM measurement WHERE unit = 'cups'), 4
UNION ALL
SELECT @mealId5, 173420, (SELECT id FROM measurement WHERE unit = 'cups'), 0.25
UNION ALL
SELECT @mealId5, 168550, (SELECT id FROM measurement WHERE unit = 'units'), 0.5
UNION ALL
SELECT @mealId5, 171413, (SELECT id FROM measurement WHERE unit = 'tbsp'), 2;