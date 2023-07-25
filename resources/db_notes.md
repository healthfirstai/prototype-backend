# Database Notes

## General Notes
- The most important file for initiating the PostGres with pgvector enabled is the init.sql file. init.sql combined the food.sql file and the nutrition_vector.sql file
- Everything else there is currently unrelated to the postgres database and should be ignored (for now)

```sql
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
                               where "Name" like 'Rasberries'))
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
```
