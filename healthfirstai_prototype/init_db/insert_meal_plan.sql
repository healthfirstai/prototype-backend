-- First, we create a meal plan
INSERT INTO `meal_plan` (`name`)
VALUES ('Default Meal Plan');

-- Then we get the ID of the meal plan we just inserted.
SET @mealPlanId = LAST_INSERT_ID();

-- Now we insert the meals
INSERT INTO `meal` (`name`, `meal_plan_id`)
VALUES ('Meal 1', @mealPlanId),
       ('Double Chocolate Cherry Smoothie', @mealPlanId),
       ('Bibb Lettuce Burger', @mealPlanId),
       ('Post-Workout Nutrition', @mealPlanId),
       ('Shrimp With Spinach Salad & Brown Rice', @mealPlanId);

-- Then we store the meal ids
SET @mealId1 = (SELECT `ID`
                FROM `meal`
                WHERE `name` = 'Meal 1'
                  AND `meal_plan_id` = @mealPlanId);
SET @mealId2 = (SELECT `ID`
                FROM `meal`
                WHERE `name` = 'Double Chocolate Cherry Smoothie'
                  AND `meal_plan_id` = @mealPlanId);
SET @mealId3 = (SELECT `ID`
                FROM `meal`
                WHERE `name` = 'Bibb Lettuce Burger'
                  AND `meal_plan_id` = @mealPlanId);
SET @mealId4 = (SELECT `ID`
                FROM `meal`
                WHERE `name` = 'Post-Workout Nutrition'
                  AND `meal_plan_id` = @mealPlanId);
SET @mealId5 = (SELECT `ID`
                FROM `meal`
                WHERE `name` = 'Shrimp With Spinach Salad & Brown Rice'
                  AND `meal_plan_id` = @mealPlanId);

-- Now we associate ingredients with meals in the `meal_ingredient` table.
-- As an example, for the first meal, we do the following:
INSERT INTO `meal_ingredient` (`meal_id`, `ingredient_id`, `measurement_id`, `quantity`)
VALUES (@mealId1, 171304, (SELECT `ID` FROM `measurement` WHERE `unit` = 'cups'), 1.5),  -- Greek Yogurt
       (@mealId1, 167755, (SELECT `ID` FROM `measurement` WHERE `unit` = 'cups'), 0.5),  -- Raspberries
       (@mealId1, 167542, (SELECT `ID` FROM `measurement` WHERE `unit` = 'cups'), 0.33), -- Granola
       (@mealId1, 171287, (SELECT `ID` FROM `measurement` WHERE `unit` = 'units'), 3); -- Eggs

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
VALUES (@mealId2, 173177, (SELECT ID FROM measurement WHERE unit = 'scoops'), 2),  -- Protein Powder
       (@mealId2, 170173, (SELECT ID FROM measurement WHERE unit = 'cups'), 0.25), -- Coconut Milk
       (@mealId2, 171719, (SELECT ID FROM measurement WHERE unit = 'cups'), 0.75), -- Cherries
       (@mealId2, 169414, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 1),    -- Flaxseeds
       (@mealId2, 169593, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 1),    -- Cocoa Powder
       (@mealId2, 175103, (SELECT ID FROM measurement WHERE unit = 'cubes'), 3),   -- Ice
       (@mealId2, 173234, (SELECT ID FROM measurement WHERE unit = 'cups'), 1); -- Water

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
VALUES (@mealId3, 169247, (SELECT ID FROM measurement WHERE unit = 'leaves'), 2), -- Lettuce
       (@mealId3, 174752, (SELECT ID FROM measurement WHERE unit = 'oz'), 8),    -- Ground Beef (95% lean)
       (@mealId3, 170457, (SELECT ID FROM measurement WHERE unit = 'slices'), 2), -- Tomato
       (@mealId3, 170000, (SELECT ID FROM measurement WHERE unit = 'slices'), 2), -- Red Onion
       (@mealId3, 168556, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 1),   -- Ketchup
       (@mealId3, 167736, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 1),   -- Mayonnaise (canola mayonnaise)
       (@mealId3, 169963, (SELECT ID FROM measurement WHERE unit = 'cups'), 1); -- Green Beans

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
VALUES (@mealId4, 173158, (SELECT ID FROM measurement WHERE unit = 'bar'), 1); -- Protein Bar

INSERT INTO meal_ingredient (meal_id, ingredient_id, measurement_id, quantity)
VALUES (@mealId5, 171971, (SELECT ID FROM measurement WHERE unit = 'oz'), 6),     -- Shrimp
       (@mealId5, 168875, (SELECT ID FROM measurement WHERE unit = 'cups'), 0.25), -- Brown Rice
       (@mealId5, 168462, (SELECT ID FROM measurement WHERE unit = 'cups'), 4),    -- Spinach
       (@mealId5, 173420, (SELECT ID FROM measurement WHERE unit = 'cups'), 0.25), -- Feta Cheese
       (@mealId5, 168550, (SELECT ID FROM measurement WHERE unit = 'units'), 0.5), -- Bell Pepper (red)
       (@mealId5, 171413, (SELECT ID FROM measurement WHERE unit = 'tbsp'), 2); -- Olive Oil (extra virgin)
