-- Get the nutrition embedding of raspberries
select *
from food
where "Name" like 'Raspberries';

select *
from nutrition_vector where "food_id" = 171971;

-- select most similar vector to the vector of raspberries
select *
from nutrition_vector
         join food f on nutrition_vector.food_id = f.id
-- where "Food Group" like 'Snacks'
order by embedding <=> (select embedding
                        from nutrition_vector
                        where "food_id" in
                              (select "id"
                               from food
                               where "Name" like 'Raspberries'))
limit 10;

-- select most similar vector to the vector of raspberries
select *
from nutrition_vector
         join food f on nutrition_vector.food_id = f.id
where "Food Group" like 'Snacks'
order by embedding <=> (select embedding
                        from nutrition_vector
                        where "food_id" in
                              (select "id"
                               from food
                               where "Name" like 'Cooked Shrimp'))
limit 10;
