create table nutrition_vector
(
    food_id   integer not null
        primary key
        references food,
    embedding vector(95)
);

alter table nutrition_vector
    owner to root;
